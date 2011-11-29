import eventlet
import sys
import re
import py
from eventlet.processes import Process, DeadProcess
from eventlet.timeout import Timeout
from eventlet.green.subprocess import Popen, PIPE, STDOUT
import eventlet

def timelimited(secs, func):
    if secs is not None:
        with Timeout(secs):
            return func()
    return func()

class StreamProcess:
    def __init__(self, args, linetimeout=None, **kwargs):
        args = list(map(str, args))
        self._popen = Popen(args, stdout=PIPE, stderr=PIPE, **kwargs)
        self.pid = self._popen.pid
        self.linetimeout = linetimeout
        self._stream = 0
        self._outstreampool = eventlet.GreenPool(2)

    def copy_outstream(self, stream, writer):
        f = getattr(self._popen, stream)
        def readout():
            try:
                while 1:
                    s = timelimited(self.linetimeout, f.readline)
                    if not s:
                        break
                    writer(s)
            except DeadProcess:
                pass
            except Timeout:
                self._popen.kill()
        self._outstreampool.spawn(readout)

    def wait_outstreams(self):
        self._outstreampool.waitall()

    def wait(self):
        return self._popen.wait()

class Detox:
    def __init__(self, setupfile):
        assert setupfile.check()
        self.setupfile = setupfile

    _rexsdistline = re.compile(".*new sdistfile to '(.+)'")
    def create_sdist(self):
        cwd = self.setupfile.dirpath()
        sp = StreamProcess(["tox", "--sdistonly"], cwd=str(cwd))
        sdist = []
        def hackout_sdist(line):
            sys.stdout.write(line)
            m = self._rexsdistline.match(line)
            if m is not None:
                sdist.append(m.group(1))
        sp.copy_outstream("stdout", hackout_sdist)
        sp.copy_outstream("stderr", sys.stderr.write)
        assert not sp.wait()
        sp.wait_outstreams()
        assert len(sdist) == 1
        self.sdistfile = s = py.path.local(sdist[0])
        assert s.check()
        return s

    def getvenv(self, name):
        cwd = self.setupfile.dirpath()
        sp = StreamProcess(["tox", "-e", name, "--venvonly"], cwd=str(cwd))
        sp.copy_outstream("stdout", sys.stdout.write)
        sp.copy_outstream("stderr", sys.stderr.write)
        sp.wait_outstreams()
        assert not sp.wait()
        # XXX
        venvdir = cwd.join(".tox", name)
        return venvdir

    def installsdist(self, sdist, venvname):
        cwd = self.setupfile.dirpath()
        sp = StreamProcess(["tox", "-e", venvname, "--usesdist", sdist,
            "--notest",], cwd=str(cwd))
        sp.copy_outstream("stdout", sys.stdout.write)
        sp.copy_outstream("stderr", sys.stderr.write)
        sp.wait_outstreams()
        assert not sp.wait()
        venvdir = cwd.join(".tox", venvname)
        return venvdir

    def runtestcommand(self, venvname):
        cwd = self.setupfile.dirpath()
        sp = StreamProcess(["tox", "-e", venvname, "--testonly",],
            cwd=str(cwd))
        sp.copy_outstream("stdout", sys.stdout.write)
        sp.copy_outstream("stderr", sys.stderr.write)
        sp.wait_outstreams()
        assert not sp.wait()
        venvdir = cwd.join(".tox", venvname)
        return venvdir


