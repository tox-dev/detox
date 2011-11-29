import eventlet
import sys
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
    def __init__(self, args, linetimeout=None):
        self._popen = Popen(args, stdout=PIPE, stderr=PIPE)
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
