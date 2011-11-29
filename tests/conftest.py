import pytest
import py
import eventlet

pytest_plugins = "pytester"

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

