from __future__ import with_statement

import eventlet
from eventlet.timeout import Timeout
from eventlet.green.subprocess import Popen
from eventlet import GreenPool
import tox
import tox.session


def timelimited(secs, func):
    if secs is not None:
        with Timeout(secs):
            return func()
    return func()

class FileSpinner:
    chars = r"- \ | / - \ | /".split()
    def __init__(self):
        self.path2last = {}

    def getchar(self, path):
        try:
            lastsize, charindex = self.path2last[path]
        except KeyError:
            lastsize, charindex = 0, 0
        newsize = path.size()
        if newsize != lastsize:
            charindex += 1
        self.path2last[path] = (lastsize, charindex)
        return self.chars[charindex % len(self.chars)]


class ToxReporter(tox.session.Reporter):
    sortorder = ("runtests command installdeps installpkg inst inst-nodeps "
        "sdist-make create recreate".split())

    def __init__(self, session):
        super(ToxReporter, self).__init__(session)
        self._actionmayfinish = set()

    def _loopreport(self):
        filespinner = FileSpinner()
        while 1:
            eventlet.sleep(0.2)
            msg = []
            ac2popenlist = {}
            for action in self.session._actions:
                for popen in action._popenlist:
                    if popen.poll() is None:
                        l = ac2popenlist.setdefault(action.activity, [])
                        l.append(popen)
                if not action._popenlist and action in self._actionmayfinish:
                    super(ToxReporter, self).logaction_finish(action)
                    self._actionmayfinish.remove(action)

            for acname in self.sortorder:
                try:
                    popenlist = ac2popenlist.pop(acname)
                except KeyError:
                    continue
                sublist = []
                for popen in popenlist:
                    name = getattr(popen.action.venv, 'name', "INLINE")
                    char = filespinner.getchar(popen.outpath)
                    sublist.append("%s%s" % (name, char))
                msg.append("%s %s" % (acname, " ".join(sublist)))
            assert not ac2popenlist, ac2popenlist
            if msg:
                msg = "   ".join(msg)
                if len(msg) >= self.tw.fullwidth:
                    msg = msg[:self.tw.fullwidth-3]+".."
                self.tw.reline(msg)

    def __getattr__(self, name):
        if name[0] == "_":
            raise AttributeError(name)

        def generic_report(*args):
            self._calls.append((name,)+args)
            if self.config.option.verbosity >= 2:
                print ("%s" %(self._calls[-1], ))
        return generic_report

    def logaction_finish(self, action):
        if action._popenlist:
            # defer finishing output to spinner loop
            self._actionmayfinish.add(action)
        else:
            super(ToxReporter, self).logaction_finish(action)

    #def logpopen(self, popen):
    #    self._tw.line(msg)

    #def popen_error(self, msg, popen):
    #    self._tw.line(msg, red=True)
    #    self._tw.line("logfile: %s" % popen.stdout.name)

class Detox:
    def __init__(self, toxconfig):
        self._toxconfig = toxconfig
        self._resources = Resources(self)

    def startloopreport(self):
        if self.toxsession.report.tw.hasmarkup:
            eventlet.spawn_n(self.toxsession.report._loopreport)

    @property
    def toxsession(self):
        try:
            return self._toxsession
        except AttributeError:
            self._toxsession = tox.session.Session(
                self._toxconfig, Report=ToxReporter, popen=Popen)
            return self._toxsession

    def provide_sdist(self):
        tox_major, tox_minor = tox.__version__.split('.')[:2]
        if int(tox_major) > 2 and int(tox_minor) > 2:
            from tox.package import get_package

            sdistpath = get_package(self.toxsession)
        else:
            sdistpath = self.toxsession.get_installpkg_path()
        if not sdistpath:
            raise SystemExit(1)
        return sdistpath

    def provide_venv(self, venvname):
        venv = self.toxsession.getvenv(venvname)
        if self.toxsession.setupenv(venv):
            return venv

    def provide_installpkg(self, venvname, sdistpath):
        venv = self.toxsession.getvenv(venvname)
        return self.toxsession.installpkg(venv, sdistpath)

    def runtests(self, venvname):
        if self.toxsession.config.option.sdistonly:
            self._sdistpath = self.getresources("sdist")
            return
        if self.toxsession.config.skipsdist:
            venv, = self.getresources("venv:%s" % venvname)
            if venv:
                venv.finish()
                self.toxsession.runtestenv(venv, redirect=True)
        else:
            venv, sdist = self.getresources("venv:%s" % venvname, "sdist")
            self._sdistpath = sdist
            if venv and sdist:
                if self.toxsession.installpkg(venv, sdist):
                    self.toxsession.runtestenv(venv, redirect=True)

    def runtestsmulti(self, envlist):
        pool = GreenPool(size=self._toxconfig.option.numproc)
        for env in envlist:
            pool.spawn_n(self.runtests, env)
        pool.waitall()
        if not self.toxsession.config.option.sdistonly:
            retcode = self._toxsession._summary()
            return retcode

    def getresources(self, *specs):
        return self._resources.getresources(*specs)

class Resources:
    def __init__(self, providerbase):
        self._providerbase = providerbase
        self._spec2thread = {}
        self._pool = GreenPool()
        self._resources = {}

    def _dispatchprovider(self, spec):
        parts = spec.split(":")
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
