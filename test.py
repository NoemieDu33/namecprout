from motor import Motor
import time,sys

mo = Motor()
mo.send_signal(1,str(sys.argv[1]))