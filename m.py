import detox
import eventlet
from detox.proc import Detox
py.path.local("../pytest/setup.py").chdir()
result = detox.main("-e", "py26,py27")

