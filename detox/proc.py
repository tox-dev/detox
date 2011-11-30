import eventlet
import sys
import py
from eventlet.processes import Process, DeadProcess
from eventlet.timeout import Timeout
from eventlet.green.subprocess import Popen, PIPE, STDOUT
from eventlet import GreenPool
import eventlet
import tox._config
import tox._cmdline

def timelimited(secs, func):
    if secs is not None:
        with Timeout(secs):
            return func()
    return func()

class Detox:
    def __init__(self, setupfile):
        setupfile = py.path.local(setupfile)
        assert setupfile.check()
        self.setupfile = setupfile
        self._resources = Resources(self)

    @property
    def toxsession(self):
        try:
            return self._toxsession
        except AttributeError:
            toxini = self.setupfile.dirpath("tox.ini")
            config = tox._config.parseconfig(['-c', str(toxini)])
            self._toxsession = tox._cmdline.Session(config, Popen)
            return self._toxsession

    def provide_sdist(self):
        return self.toxsession.sdist()


    def provide_venv(self, venvname):
        venv = self.toxsession.getvenv(venvname)
        self.toxsession.setupenv(venv, None)
        return venv

    def runtests(self, venvname):
        venv, sdist = self.getresources("venv:%s" % venvname, "sdist")
        venv.install_sdist(sdist)
        venv.test()

    def getresources(self, *specs):
        return self._resources.getresources(*specs)

class Resources:
    def __init__(self, providerbase):
        self._providerbase = providerbase
        self._spec2thread = {}
        self._pool = GreenPool(1000)
        self._resources = {}

    def _dispatchprovider(self, spec):
        parts = spec.split(":", 1)
        name = parts.pop(0)
        provider = getattr(self._providerbase, "provide_" + name)
        self._resources[spec] = res = provider(*parts)
        return res

    def getresources(self, *specs):
        for spec in specs:
            if spec not in self._resources:
                if spec not in self._spec2thread:
                    t = self._pool.spawn(self._dispatchprovider, spec)
                    self._spec2thread[spec] = t
        l = []
        for spec in specs:
            if spec not in self._resources:
                self._spec2thread[spec].wait()
            l.append(self._resources[spec])
        return l
