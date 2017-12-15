import snort_mysql as mysql
import odl_send
import socket
import sys
import time
from odl_send import old_flow


if __name__ == "__main__":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('140.126.130.42', 8001))
        while True:
            select = str(sock.recv(1024).decode('utf-8'))
            if not select:
                pass
            else:
                mysql.mysql_select("select inet_ntoa(ip_src),count(*) from iphdr group by ip_src")
                time.sleep(15)
                sock.send(select.encode('utf-8'))
                print("收到: " + select)
    except KeyboardInterrupt:
        print("Ctrl-c pressed ...")
        sys.exit()