import requests
from requests.auth import HTTPBasicAuth

class old_flow:
    node = "openflow:198558770832580"
    tableID = "0"
    headers = {'Content-Type': 'application/json'}

def Instruction(flow_id,flow_ip):
    jstr = "{'flow': [{'id': "+str(flow_id)+",'match': {'ethernet-match': {'ethernet-type': {'type': '2048'}},'ipv4-source-address-no-mask': "+str(flow_ip)+"},'flow-name': 'FuckYouBitch2','priority': '12','table_id':"+str(old_flow.tableID)+"}]}"

    url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str(old_flow.node) + '/flow-node-inventory:table/' + str(old_flow.tableID) + '/flow/' + str(flow_id)
    resp = requests.put(url, jstr, headers=old_flow.headers, auth=HTTPBasicAuth('admin', 'fu. 1u/3t/6'))
    print(resp.status_code)

def Delete_All():
    jstr = "{'table': [{'id': '0'}]}"
    url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str(old_flow.node) + '/flow-node-inventory:table/' + str(old_flow.tableID)
    resp = requests.put(url, jstr, headers=old_flow.headers, auth=HTTPBasicAuth('admin', 'fu. 1u/3t/6'))

    old_flow.ID = 0
    if resp.status_code == 200:
        print("Clear All success")
def Delete_One(flow_id):
    url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str(old_flow.node) + '/flow-node-inventory:table/' + str(old_flow.tableID)+ '/flow/' + str(flow_id)
    resp = requests.delete(url, headers=old_flow.headers, auth=HTTPBasicAuth('admin', 'fu. 1u/3t/6'))

    if resp.status_code == 200:
        print("Clear Table "+flow_id+" success")
def Find_All(option , flow):
    url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str(
        old_flow.node) + '/flow-node-inventory:table/' + str(old_flow.tableID)
    resp = requests.get(url, headers=old_flow.headers, auth=HTTPBasicAuth('admin', 'fu. 1u/3t/6'))

    if resp.text == """{"flow-node-inventory:table":[{"id":0}]}""":
        print("OpenDayLight flow table "+old_flow.tableID+" is empty")
    else:
        line = resp.text.strip('{ } [ ] "').split(',')
        del line[0:1]
        line[0] = line[0][8:]

        next_id, next_priority, next_ip = False, False, False

        for i in line:
            for j in i.split(':'):
                if """{"id\"""" in j:
                    next_id = True
                elif """\"priority\"""" in j:
                    next_priority = True
                elif """{\"ipv4-source-address-no-mask\"""" in j:
                    next_ip = True
                elif next_id == True:
                    flow.id.append(j.strip('"'))
                    next_id = False
                elif next_priority == True:
                    flow.priority.append(j)
                    next_priority = False
                elif next_ip == True:
                    if j.strip('"') not in flow.ip:
                        flow.ip.append(j.strip('"'))
                        flow.id_count = flow.id_count + 1
                    next_ip = False
        if option == 1:
            print(" ------------------------------------")
            print("∥%7s∥%8s∥%s∥" % ("Flow ID", "Priority", "IP".center(15)))
            print(" ------------------------------------")
            for i in range(flow.id_count-1):
                print("∥%s∥%s∥%-15s∥" % (flow.id[i].center(7), flow.priority[i].center(8), flow.ip[i]))
                print(" ------------------------------------")




