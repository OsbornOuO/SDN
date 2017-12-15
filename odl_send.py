import requests
from requests.auth import HTTPBasicAuth

class old_flow:
    ID = 0
    def add ():
        old_flow.ID+=1
def odl_send_instruction(ip_addr):

    ofs_node = "openflow:198558770832580"
    ofs_tableID = "0"


    jstr = "{'flow': [{'id': "+str(old_flow.ID)+",'match': {'ethernet-match': {'ethernet-type': {'type': '2048'}},'ipv4-source-address-no-mask': "+str(ip_addr)+"},'flow-name': 'FuckYouBitch2','priority': '12','table_id':"+str(ofs_tableID)+"}]}"

    url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str( ofs_node) + '/flow-node-inventory:table/' + str(ofs_tableID) + '/flow/' + str(old_flow.ID)
    headers = {'Content-Type': 'application/json'}
    resp = requests.put(url, jstr, headers=headers, auth=HTTPBasicAuth('admin', 'fu. 1u/3t/6'))
    print(resp.status_code)
    old_flow.add()

def odl_send_delete():
    ofs_node = "openflow:198558770832580"
    ofs_tableID = "0"

    jstr = "{'table': [{'id': '0'}]}"

    url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str(ofs_node) + '/flow-node-inventory:table/' + str(ofs_tableID)
    headers = {'Content-Type': 'application/json'}
    resp = requests.put(url, jstr, headers=headers, auth=HTTPBasicAuth('admin', 'fu. 1u/3t/6'))

    old_flow.ID = 0
    print(resp.status_code)

def odl_send_find():
    ofs_node = "openflow:198558770832580"
    ofs_tableID = "0"

    url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str(
        ofs_node) + '/flow-node-inventory:table/' + str(ofs_tableID)
    headers = {'Content-Type': 'application/json'}
    resp = requests.get(url, headers=headers, auth=HTTPBasicAuth('admin', 'fu. 1u/3t/6'))

    line = resp.text.strip('{ } [ ] "').split(',')
    del line[0:1]
    line[0] = line[0][8:]

    next_id = False
    next_priority = False
    next_ip = False

    flow_id = []
    priority = []
    ip = []

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
    print(" ------------------------------------")
    print("∥%7s∥%8s∥%s∥" % ("Flow ID", "Priority", "IP".center(15)))
    print(" ------------------------------------")
    for i in range(len(ip)):
        print("∥%s∥%s∥%-15s∥" % (flow_id[i].center(7), priority[i].center(8), ip[i]))
        print(" ------------------------------------")




