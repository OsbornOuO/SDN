import os
from idstools import unified2
from glob import glob

import datetime
import pyinotify


class MyEventHandler(pyinotify.ProcessEvent):
    # 自定义写入那个文件，可以自己修改

    def process_IN_ACCESS(self, event):
        print("ACCESS event:", event.pathname)
    def process_IN_ATTRIB(self, event):
        print("ATTRIB event:", event.pathname)
    def process_IN_CLOSE_NOWRITE(self, event):
        print("CLOSE_NOWRITE event:", event.pathname)
    def process_IN_CLOSE_WRITE(self, event):
        print("CLOSE_WRITE event:", event.pathname)
    def process_IN_CREATE(self, event):
        print("CREATE event:", event.pathname)
    def process_IN_DELETE(self, event):
        print ("DELETE event:", event.pathname)
    def process_IN_MODIFY(self, event):
        print("MODIFY event:", event.pathname)
    def process_IN_OPEN(self, event):
        print("OPEN event:", event.pathname)

wm = pyinotify.WatchManager()
wm.add_watch("C:\\Users\OSBORN\Desktop", pyinotify.ALL_EVENTS, rec=True)
# /tmp是可以自己修改的监控的目录
# event handler
# eh = MyEventHandler()

# notifier
notifier = pyinotify.Notifier(wm, eh)
notifier.loop()