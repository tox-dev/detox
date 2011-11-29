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

