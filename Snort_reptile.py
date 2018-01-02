#/usr/bin/Python3
#coding = UTF-8

from watchdog.observers import Observer
from watchdog.events import *
import time
import socket
import threading

class Check:
      two = 0
      status = False
      
class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
          FileSystemEventHandler.__init__(self)
    def on_modified(self, event):
          if Check.two == 1:
                Check.status = True
                Check.two = 0
          else:
                Check.two = 1


observer = Observer()
event_handler = FileEventHandler()
#observer.schedule(event_handler,"C:\\Users\OSBORN\Desktop",True)
observer.schedule(event_handler,"/var/log/snort/",True)
observer.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.bind(('127.0.0.1', 8001))
sock.bind(('140.126.130.42', 8001))
sock.listen(5)
print('server start...')

try:
      while True:
            connection,address = sock.accept()
            try:
                  print('Client is online '+str(address[0]))
                  connection.settimeout(600)
                  while True:
                        if Check.status == True:
                              Check.status = False
                              connection.send('Update Flow'.encode('utf-8'))
                              buf = connection.recv(1024)
                              print(str(address[0]),buf.decode("utf-8"))
            except ConnectionAbortedError:
                  print('Client is offline'+str(address))
                  continue
            except ConnectionResetError:
                  print('Client is offline'+str(address))
                  continue
            except socket.timeout:
                  print('time out')
                  continue
            finally:
                  connection.close()
                  continue
except KeyboardInterrupt:
      observer.stop()
finally:
      print('Close Socket')
      sock.close()
observer.join()
