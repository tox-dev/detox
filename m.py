import detox
import eventlet
from detox.proc import Detox
dt = Detox("../pytest/setup.py")
dt.runtests("py26")
