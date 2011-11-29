import detox
import eventlet
from detox.proc import Detox
dt = Detox("../pytest/setup.py")
sdist = dt.create_sdist()
def create_venv_and_test(name, sdist):
    dt.getvenv(name)
    dt.installsdist(sdist, name)
    dt.runtestcommand(name)

pool = eventlet.GreenPool()
pool.spawn(lambda: create_venv_and_test("py26", sdist))
pool.spawn(lambda: create_venv_and_test("py27", sdist))
pool.waitall()


