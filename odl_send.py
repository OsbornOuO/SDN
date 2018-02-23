import requests
from requests.auth import HTTPBasicAuth

class odl_flow:
#   node ="openflow:198558770832580"
    node =["openflow:336185077760","openflow:198558770832580"]
    tableID = "0"
    headers = {'Content-Type': 'application/json'}
    account = HTTPBasicAuth('admin', 'fu. 1u/3t/6')
    baseUrl = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/'
    def putData(Long_url,jstr):
        return requests.put(Long_url,jstr,headers=odl_flow.headers,auth=odl_flow.account)
    def deleteData(Long_url):
        return requests.delete(Long_url,headers=odl_flow.headers,auth=odl_flow.account)
    def getData(Long_url):
        return requests.get(Long_url,headers=odl_flow.headers,auth = odl_flow.account)

def Instruction(flow_id,flow_ip):
    for node in odl_flow.node:
        jstr = "{'flow': [{'id': "+str(flow_id)+",'match': {'ethernet-match': {'ethernet-type': {'type': '2048'}},'ipv4-source-address-no-mask': "+\
            str(flow_ip)+"},'flow-name': 'FuckYouBitch2','priority': '12','table_id':"+str(odl_flow.tableID)+"}]}"
        url = odl_flow.baseUrl + str(node) + '/flow-node-inventory:table/' + str(odl_flow.tableID) + '/flow/' + str(flow_id)
        req = odl_flow.putData(url,jstr).status_code
        if req == 201:
            print("Switch【%-25s】 Add flow with ip :%s "%(node.center(25),flow_ip))
        elif req == 200:
            print("Switch【%-25s】 Add flow with ip :%s "%(node.center(25),flow_ip))
        elif req == 400:
            print("Switch【%-25s】 Fail to add flow :%s "%(node.center(25),flow_ip))

def Delete_All():
    for node in odl_flow.node:
        jstr = """{"table": [{"id": "0"}]}"""
        url = odl_flow.baseUrl + str(node) + '/flow-node-inventory:table/' + str(odl_flow.tableID)
        if odl_flow.putData(url,jstr).status_code == 200:
            print("Switch【%-25s】Clear All success"%(node.center(25)))
def Delete_One(flow_id):
    for node in odl_flow.node:
        url = odl_flow.baseUrl + str(node) + '/flow-node-inventory:table/' + str(odl_flow.tableID)+'/flow/' + str(flow_id)
        if odl_flow.deleteData(url).status_code == 200:
            print("Switch【%-25s】Delete Flow Table ID : 【"%(node.center(25))+flow_id+"】success")
def Find_All(option , flow):
    for node in odl_flow.node:
        url = 'http://140.126.130.44:8181/restconf/config/opendaylight-inventory:nodes/node/' + str(
            node) + '/flow-node-inventory:table/' + str(odl_flow.tableID)
        resp = odl_flow.getData(url)

        if resp.text == """{"flow-node-inventory:table":[{"id":0}]}""":
            print("Switch【%25s】flow table "%(node.center(25))+odl_flow.tableID+" is empty")
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
                print("【%-25s】switch Table :"%(node.center(25)))
                print(" ========================================= ")
                print("∥%7s∥%8s∥%20s∥" % ("Flow ID", "Priority", "IP".center(20)))
                print(" ========================================= ")
                for i in range(flow.id_count):
                    print("∥%s∥%s∥%-20s∥" % (flow.id[i].center(7), flow.priority[i].center(8), flow.ip[i].center(20)))
                    print(" ========================================= ")
                print()




