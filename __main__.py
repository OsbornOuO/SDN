import snort_mysql as mysql
import odl_send
import socket
import sys
import time
import getopt

class flow:
    id_count = 0
    id = []
    priority = []
    ip = []

def Dump_Flow():
    odl_send.Find_All(0, flow)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            sock.connect(('127.0.0.1', 8001))
            print("Connect to Server")
            while True:
                select = str(sock.recv(1024).decode('utf-8'))
                if select:
                    print("Server Request : " + select)
                    mysql.mysql_select(0,"select inet_ntoa(ip_src),count(*) from iphdr group by ip_src", flow)
                    sock.send("更新完畢".encode('utf-8'))
                else:
                    pass
        except ConnectionRefusedError:
            print("無法連線，因為目標電腦拒絕連線,等待五秒再連線")
            time.sleep(5)
            continue
def Delete_odl_Table():
    odl_send.Delete_All()
def Find_odl_Table():
    odl_send.Find_All(1, flow)
if __name__ == "__main__":
    ip = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hrDd:s',["ip="])
    except getopt.GetoptError:
        sys.exit(2)
    try:
        for opt, arg in opts:
            if opt == '-h':
                print(
                    "%-20s:%s"%("-r","Start add flow\n")+
                    "%-20s:%s"%("-d (ipv4 address)","Delete flow by input ipv4\n")+
                    "%-20s:%s"%("-D","Delete all flow\n")+
                    "%-20s:%s"%("-s","Search OpenDayLight all flow\n")
                )
            elif opt in ('-r'):
                Dump_Flow()
            elif opt in ('-d',"--ip"):
                odl_send.Find_All(0, flow)
                try:
                    mysql.mysql_select(1,
                                       "DELETE from iphdr WHERE inet_ntoa(ip_src) = '" + arg + "'",
                                       flow.id[flow.ip.index(arg)]
                                       )
                except ValueError:
                    print("This ip is not in Flow Table "+ arg)
                if arg in flow.ip:
                    flow.id.pop(flow.ip.index(arg))
                    flow.priority.pop(flow.ip.index(arg))
                    flow.ip.remove(arg)
            elif opt in ('-D'):
                Delete_odl_Table()
            elif opt in ('-s'):
                Find_odl_Table()
            else:
                print("?")
    except KeyboardInterrupt:
        print("結束")
        sys.exit()