import eventlet
import sys
import re
import py
from eventlet.processes import Process, DeadProcess
from eventlet.timeout import Timeout
from eventlet.green.subprocess import Popen, PIPE, STDOUT
import eventlet
import tox._config
import tox._cmdline

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
        setupfile = py.path.local(setupfile)
        assert setupfile.check()
        self.setupfile = setupfile

    @property
    def toxsession(self):
        try:
            return self._toxsession
        except AttributeError:
            toxini = self.setupfile.dirpath("tox.ini")
            config = tox._config.parseconfig(['-c', str(toxini)])
            self._toxsession = tox._cmdline.Session(config, Popen)
            return self._toxsession

    _rexsdistline = re.compile(".*new sdistfile to '(.+)'")
    def create_sdist(self):
        sdist = self.toxsession.sdist()
        return sdist

    def gettoxenv(self, venvname):
        venv = session.getvenv(venvname)
        return venv.envdir

    def getvenv(self, venvname):
        venv = self.toxsession.getvenv(venvname)
        self.toxsession.setupenv(venv, None)
        return venv.envconfig.envdir

    def installsdist(self, sdist, venvname):
        venv = self.toxsession.getvenv(venvname)
        venv.install_sdist(sdist)
        return venv

    def runtestcommand(self, venvname):
        venv = self.toxsession.getvenv(venvname)
        venv.test()


