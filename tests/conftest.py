from __future__ import with_statement
import pytest
import py
import time
import sys
import eventlet
import detox
from py.builtin import print_
from eventlet.green.subprocess import Popen
from textwrap import dedent as d
from detox.proc import Detox
from _pytest.pytester import RunResult, getdecoded
import detox.main

pytest_plugins = "pytester"

def create_example1(tmpdir):
    tmpdir.join("setup.py").write(d("""
        from setuptools import setup

        def main():
            setup(
                name='example1',
                description='example1 project for testing detox',
                version='0.4',
                packages=['example1',],
            )
        if __name__ == '__main__':
            main()
    """))
    tmpdir.join("tox.ini").write(d("""
        [testenv:py]
    """))
    tmpdir.join("example1", "__init__.py").ensure()


def create_example2(tmpdir):
    tmpdir.join("tox.ini").write(d("""
        [tox]
        skipsdist = True

        [testenv:py]
    """))
    tmpdir.join("example2", "__init__.py").ensure()


def create_example3(tmpdir):
    tmpdir.join("tox.ini").write(d("""
        [tox]
        skipsdist = True

        [testenv]
        commands = python -c 'import time; time.sleep(1)'

        [testenv:py1]
        [testenv:py2]
    """))
    tmpdir.join("example3", "__init__.py").ensure()


def pytest_configure(config):
    config.addinivalue_line("markers", "example1: use example1 for setup")
    config.addinivalue_line("markers", "example2: use example2 for setup")
    config.addinivalue_line("markers", "timeout(N): stop test function "
        "after N seconds, throwing a Timeout.")

def pytest_funcarg__exampledir(request):
    tmpdir = request.getfuncargvalue("tmpdir")
    for x in dir(request.function):
        if x.startswith("example"):
            exampledir = tmpdir.mkdir(x)
            globals()["create_"+x](exampledir)
            print ("%s created at %s" %(x,exampledir))
            break
    else:
        raise request.LookupError("test function has example")
    return exampledir

def pytest_funcarg__detox(request):
    exampledir = request.getfuncargvalue("exampledir")
    old = exampledir.chdir()
    try:
        return Detox(detox.main.parse([]))
    finally:
        old.chdir()

def pytest_funcarg__cmd(request):
    exampledir = request.getfuncargvalue("exampledir")
    cmd = Cmd(exampledir, request)
    return cmd

class Cmd:
    def __init__(self, basedir, request):
        self.basedir = basedir
        self.tmpdir = basedir.mkdir(".cmdtmp")
        self.request = request

    def main(self, *args):
        self.basedir.chdir()
        return detox.main.main(args)

    def rundetox(self, *args):
        old = self.basedir.chdir()
        script = py.path.local.sysfind("detox")
        assert script, "could not find 'detox' script"
        return self._run(script, *args)

    def _run(self, *cmdargs):
        cmdargs = [str(x) for x in cmdargs]
        p1 = self.tmpdir.join("stdout")
        p2 = self.tmpdir.join("stderr")
        print_("running", cmdargs, "curdir=", py.path.local())
        f1 = p1.open("wb")
        f2 = p2.open("wb")
        now = time.time()
        popen = Popen(cmdargs, stdout=f1, stderr=f2,
            close_fds=(sys.platform != "win32"))
        ret = popen.wait()
        f1.close()
        f2.close()
        out = p1.read("rb")
        out = getdecoded(out).splitlines()
        err = p2.read("rb")
        err = getdecoded(err).splitlines()
        def dump_lines(lines, fp):
            try:
                for line in lines:
                    py.builtin.print_(line, file=fp)
            except UnicodeEncodeError:
                print("couldn't print to %s because of encoding" % (fp,))
        dump_lines(out, sys.stdout)
        dump_lines(err, sys.stderr)
        return RunResult(ret, out, err, time.time()-now)

@pytest.mark.tryfirst
def pytest_pyfunc_call(__multicall__, pyfuncitem):
    try:
        timeout = pyfuncitem.obj.timeout.args[0]
    except (AttributeError, IndexError):
        timeout = 5.0
    with eventlet.Timeout(timeout):
        return __multicall__.execute()

def test_pyfuncall():
    class MC:
        def execute(self):
            eventlet.sleep(5.0)
    class pyfuncitem:
        class obj:
            class timeout:
                args = [0.001]
    pytest.raises(eventlet.Timeout,
        lambda: pytest_pyfunc_call(MC(), pyfuncitem))

def test_hang(testdir):
    p = py.path.local(__file__).dirpath('conftest.py')
    p.copy(testdir.tmpdir.join(p.basename))
    t = testdir.makepyfile("""
        import pytest
        from eventlet.green import time
        @pytest.mark.timeout(0.01)
        def test_hang():
            time.sleep(3.0)
    """)
    result = testdir.runpytest()
    assert "failed to timeout" not in result.stdout.str()
    result.stdout.fnmatch_lines(["*Timeout: 0.01*"])
