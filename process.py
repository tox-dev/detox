import eventlet
import sys
from eventlet.processes import Process, DeadProcess
from eventlet.timeout import Timeout
from eventlet.green.subprocess import Popen, PIPE, STDOUT

def timelimited(secs, func):
    with Timeout(secs):
        return func()

def create_process(sendresult, args):
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    pid = p.pid
    sendresult("processstarted", pid, args)
    convert_pipe(sendresult, p, "stdout")
    convert_pipe(sendresult, p, "stderr")

def convert_pipe(sendresult, p, cmd, timeout=1.0):
    sourcepipe = getattr(p, cmd)
    def sending():
        try:
            while 1:
                s = timelimited(1.0, sourcepipe.readline)
                if not s:
                    break
                sendresult(cmd, s)
        except DeadProcess:
            pass
        except Timeout:
            sendresult("%s-linetimeout" % cmd)
            p.kill()
        p.wait()
        sendresult("%s-finished" % cmd, p.pid)
    eventlet.spawn_n(sending)

if __name__ == "__main__":
    q = eventlet.Queue()
    def sender(*args):
        q.put(args)
    args = sys.argv[1:] or ["ls"]
    subspawn = eventlet.spawn(lambda: create_process(sender, args))
    counter = 0
    while 1:
        resultitem = q.get()
        if resultitem is None:
            break
        print resultitem
        if resultitem[0].endswith("-finished"):
            counter += 1
            if counter >= 2:
                break

