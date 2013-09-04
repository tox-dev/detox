import pytest
import eventlet
import detox
from detox.proc import Resources

class TestResources:
    def test_getresources(self):
        l= []
        class Provider:
            def provide_abc(self):
                l.append(1)
                return 42
        resources = Resources(Provider())
        res, = resources.getresources("abc")
        assert res == 42
        assert len(l) == 1
        res, = resources.getresources("abc")
        assert len(l) == 1
        assert res == 42

    def test_getresources_param(self):
        class Provider:
            def provide_abc(self, param):
                return param
        resources = Resources(Provider())
        res, = resources.getresources("abc:123")
        return res == "123"

    def test_getresources_parallel(self):
        l= []
        queue = eventlet.Queue()
        class Provider:
            def provide_abc(self):
                l.append(1)
                return 42
        resources = Resources(Provider())
        pool = eventlet.GreenPool(2)
        pool.spawn(lambda: resources.getresources("abc"))
        pool.spawn(lambda: resources.getresources("abc"))
        pool.waitall()
        assert len(l) == 1

    def test_getresources_multi(self):
        l= []
        queue = eventlet.Queue()
        class Provider:
            def provide_abc(self):
                l.append(1)
                return 42
            def provide_def(self):
                l.append(1)
                return 23
        resources = Resources(Provider())
        a, d = resources.getresources("abc", "def")
        assert a == 42
        assert d == 23

class TestDetoxExample1:
    pytestmark = [pytest.mark.example1, pytest.mark.timeout(20)]

    def test_createsdist(self, detox):
        sdist, = detox.getresources("sdist")
        assert sdist.check()

    def test_getvenv(self, detox):
        venv, = detox.getresources("venv:py")
        assert venv.envconfig.envdir.check()
        venv2, = detox.getresources("venv:py")
        assert venv == venv2

    def test_test(self, detox):
        detox.runtests("py")

class TestCmdline:
    pytestmark = [pytest.mark.example1]
    @pytest.mark.timeout(20)
    def test_runtests(self, cmd):
        result = cmd.rundetox("-e", "py", "-v", "-v")
        result.stdout.fnmatch_lines([
            "py*getenv*",
            "py*create:*",
        ])
