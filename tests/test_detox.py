import pytest
from detox.proc import StreamProcess
import eventlet

@pytest.mark.parametrize(("stream", "value",), [
    ("stdout", "a", ),
    ("stdout", "a\n", ),
    ("stderr", "b13\n17", ),
])
def test_subprocess_outstreams(stream, value):
    sp = StreamProcess(["python", "-c",
        "import sys ; sys.%s.write(%r)" % (stream, value)])
    l = []
    sp.copy_outstream(stream, l.append)
    sp.wait_outstreams()
    result = "".join(l)
    assert result == value

def test_subprocess_linetimeout():
    sp = StreamProcess(["python", "-c",
        "import time ; time.sleep(5)"], linetimeout=0.01)
    sp.copy_outstream("stdout", lambda d: None)
    sp.wait_outstreams()
    ret = sp.wait()
    assert ret
    assert ret == -9
