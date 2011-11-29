import pytest
from detox.proc import StreamProcess
import eventlet

class TestStreamProcess:
    @pytest.mark.parametrize(("stream", "value",), [
        ("stdout", "a", ),
        ("stdout", "a\n", ),
        ("stderr", "b13\n17", ),
    ])
    def test_outstreams(self, stream, value):
        sp = StreamProcess(["python", "-c",
            "import sys ; sys.%s.write(%r)" % (stream, value)])
        l = []
        sp.copy_outstream(stream, l.append)
        sp.wait_outstreams()
        result = "".join(l)
        assert result == value

    @pytest.mark.parametrize("stream", ["stdout", "stderr"])
    def test_outstreams_linetimeout(self, stream):
        sp = StreamProcess(["python", "-c",
            "import time ; time.sleep(5)"], linetimeout=0.01)
        sp.copy_outstream(stream, lambda d: None)
        sp.wait_outstreams()
        ret = sp.wait()
        assert ret
        assert ret == -9


class TestDetox:
    @pytest.mark.example1
    def test_createsdist(self, detox):
        assert detox.setupfile.check()
        sdist = detox.createsdist()
        assert sdist.check()

