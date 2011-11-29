import pytest
import py
import eventlet
from textwrap import dedent as d
from detox.proc import Detox

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
    """))
    tmpdir.join("example1", "__init__.py").ensure()

def pytest_configure(config):
    config.addinivalue_line("markers", "example1: use example1 for setup")
    config.addinivalue_line("markers", "timeout(N): stop test function "
        "after N seconds.")

def pytest_funcarg__detox(request):
    tmpdir = request.getfuncargvalue("tmpdir")
    for x in dir(request.function):
        if x.startswith("example"):
            exampledir = tmpdir.mkdir(x)
            globals()["create_"+x](exampledir)
            print ("%s created at %s" %(x,exampledir))
            break
    else:
        raise request.LookupError("test function does not define example")
    return Detox(exampledir.join("setup.py"))

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

