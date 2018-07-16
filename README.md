# SDN
### Use OpenDaylight , Snort2.9.11 , mysql , python3.6 , Open vSwitch
# 實體網路結構圖
![拓譜圖](https://github.com/OsbornOuO/SDN/blob/master/%E6%8B%93%E8%AD%9C.png)
# 流程圖
![流程圖](https://github.com/OsbornOuO/SDN/blob/master/%E6%B5%81%E7%A8%8B%E5%9C%96.png)

# 自動化防禦區域內網路
## 實驗目的
1. 保護區域內的網路(Switch B 底下的網域)
2. 可自動化的新增Flow 達到不需要人員控管
3. 依照Snort 設定的偵測 可偵測不同類型的攻擊

## 環境設定
1. Snort 2.9.11 [建立文件](https://s3.amazonaws.com/snort-org-site/production/document_files/files/000/000/122/original/Snort_2.9.9.x_on_Ubuntu_14-16.pdf)
2. OpenDaylight
3. Open vSwitch 

## 使用到的技術
1. Socket使用
2. HttpRequest (POST/GET)
3. 命令行參數
4. OpenDayligth API 使用方式

## 研究成果
1. 達到流量超過設定值時，自動下達Flow 給 Switch
2. 成功阻斷HostB的DDos攻擊


# 流程
1. Snort 開啟 SocketServcer 等待被連線
2. Controller(Client) 連線到 Snort (Server)
3. HostB 開始 DDos hostB
4. Snort 偵測到 流量超過設定值
5. Server 傳送要求給 Clinet
6. Client 接收到要求 到 Snort Database 抓取 alert source ip
7. Controller 下發阻擋 source ip 的 flow 給 Switch A , Switch B
8. HostB 無法發送任何封包通過 Switch A


# DOWNLOAD
```
    pip install pymysql
    pip install requests
    pip install socket
    pip install watchdog
```
+ pymysql -> connect to mysql
+ requests -> connect to OpenDaylight
+ socket -> connect Snort to controller
+ watchdog -> Listen log folder

## \__main\__.py
```
> python __main__.py -r
```
1. 於Controller上，會去連接Snort主機上的 Snort_reptile.py  
等待 Snort_reptile 傳送更新 FlowTable的要求
2. 如果接收到要求時 Controller 會去查詢 MySQL 產生 alert 的資料表  
取得所有 alert 的 source ip 
3. POST source ip 到 OpenDaylight  
OpenDaylight會再將要求傳送到指定OpenVSwtich的FlowTable(指定全部連上Controller的Swicth)
```
> python __main__.py -a XXX.XXX.XXX.XXX
```
1. 直接手動新增 flow , ip為 XXX.XXX.XXX.XXX 到 OpenDaylight
2. OpenDaylight 會再透過自己的通訊協定給OpenVSwitch
```
> python __main__.py -d XXX.XXX.XXX.XXX
```
1. 直接手動刪除 flow , ip為 XXX.XXX.XXX.XXX 到 OpenDaylight
2. OpenDaylight 會再透過自己的通訊協定給OpenVSwitch
```
> python __main__.py -D
```
1. POST FlowTable 的要求給 OpenDaylight
2. OpenDaylight 會再透過自己的通訊協定給OpenVSwitch

```
> python __main__.py -D
```
1. GET FlowTable 的要求給 OpenDaylight
2. 顯示所有在 OpenVswithc 上的 Flow 有哪些


## Snort_reptile.py
主要用於監聽Snort接收到alert時產生出.log的資料夾  
如果資料夾有更動了會傳送給連接Snort的Client  

