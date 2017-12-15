import requests
from requests.auth import HTTPBasicAuth

class old_flow:
    ID = 0
    node = "openflow:198558770832580"
    tableID = "0"
    headers = {'Content-Type': 'application/json'}

def Instruction(ip_addr):
    jstr = "{'flow': [{'id': "+str(old_flow.ID)+",'match': {'ethernet-match': {'ethernet-type': {'type': '2048'}},'ipv4-source-address-no-mask': "+str(ip_addr)+"},'flow-name': 'FuckYouBitch2','priority': '12','table_id':"+str(old_flow.tableID)+"}]}"

    url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str(old_flow.node) + '/flow-node-inventory:table/' + str(old_flow.tableID) + '/flow/' + str(old_flow.ID)
    resp = requests.put(url, jstr, headers=old_flow.headers, auth=HTTPBasicAuth('admin', 'fu. 1u/3t/6'))
    print(resp.status_code)
    old_flow.ID+=1

def Delete_All():
    jstr = "{'table': [{'id': '0'}]}"
    url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str(old_flow.node) + '/flow-node-inventory:table/' + str(old_flow.tableID)
    resp = requests.put(url, jstr, headers=old_flow.headers, auth=HTTPBasicAuth('admin', 'fu. 1u/3t/6'))

    old_flow.ID = 0
    print(resp.status_code)
def Find_All(option , ip_table):
    url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str(
        old_flow.node) + '/flow-node-inventory:table/' + str(old_flow.tableID)
    resp = requests.get(url, headers=old_flow.headers, auth=HTTPBasicAuth('admin', 'fu. 1u/3t/6'))

    if resp.text == """{"flow-node-inventory:table":[{"id":0}]}""":
        print("OpenDayLight Table:"+old_flow.tableID+" is empty")
    else:
        line = resp.text.strip('{ } [ ] "').split(',')
        del line[0:1]
        line[0] = line[0][8:]

        next_id, next_priority, next_ip = False, False, False
        flow_id, priority, ip = [], [], []

        for i in line:
            for j in i.split(':'):
                if """{"id\"""" in j:
                    next_id = True
                elif """\"priority\"""" in j:
                    next_priority = True
                elif """{\"ipv4-source-address-no-mask\"""" in j:
                    next_ip = True
                elif next_ip == True:
                    ip.append(j.strip('"'))
                    next_ip = False
                elif next_priority == True:
                    priority.append(j)
                    next_priority = False
                elif next_id == True:
                    flow_id.append(j.strip('"'))
                    next_id = False
        if option == 1:
            print(" ------------------------------------")
            print("∥%7s∥%8s∥%s∥" % ("Flow ID", "Priority", "IP".center(15)))
            print(" ------------------------------------")
            for i in range(len(ip)):
                if flow_id[i] not in ip_table:
                    ip_table.setdefault(ip[i])
                print("∥%s∥%s∥%-15s∥" % (flow_id[i].center(7), priority[i].center(8), ip[i]))
                print(" ------------------------------------")




