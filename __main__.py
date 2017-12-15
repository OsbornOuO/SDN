import snort_mysql as mysql
import odl_send
import socket
import sys
import time
import getopt

class ip:
    table = dict()
def Dump_Flow():
    odl_send.Find_All(0, ip.table)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            sock.connect(('140.126.130.42', 8001))
            while True:
                select = str(sock.recv(1024).decode('utf-8'))
                if not select:
                    pass
                else:
                    print("收到: " + select )
                    mysql.mysql_select("select inet_ntoa(ip_src),count(*) from iphdr group by ip_src", ip.table)
                    sock.send("已更新".encode('utf-8'))
        except ConnectionRefusedError:
            print("無法連線，因為目標電腦拒絕連線,等待五秒再連線")
            time.sleep(5)
            continue
def Delete_odl_Table():
    odl_send.Delete_All()
def Find_odl_Table():
    odl_send.Find_All(1, ip.table)

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],'rds')
    except getopt.GetoptError:
        sys.exit(2)
    try:
        for opt, arg in opts:
            if opt in ('-r', '--run'):
                Dump_Flow()
            elif opt in ('-d', '--delete'):
                Delete_odl_Table()
            elif opt in ('-s', '--search'):
                Find_odl_Table()
            else:
                sys.exit(2)
    except KeyboardInterrupt:
        print("結束")
        sys.exit()