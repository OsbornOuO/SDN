# SDN
Use OpenDaylight , Snort2.9.11 , mysql ,python3.6

![拓譜圖](https://github.com/OsbornOuO/SDN/blob/master/%E6%8B%93%E8%AD%9C.png)

## DOWNLOAD
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
python __main__.py -r
```
1. 於Controller上，會去連接Snort主機上的 Snort_reptile.py  
等待 Snort_reptile 傳送更新 FlowTable的要求
2. 如果接收到要求時 Controller 會去查詢 MySQL 產生 alert 的資料表  
取得所有 alert 的 source ip 
3. POST source ip 到 OpenDaylight  
OpenDaylight會再將要求傳送到指定OpenVSwtich的FlowTable(指定全部連上Controller的Swicth)
```
python __main__.py -a XXX.XXX.XXX.XXX
```
1. 直接手動新增 flow , ip為 XXX.XXX.XXX.XXX 到 OpenDaylight
2. OpenDaylight 會再透過自己的通訊協定給OpenVSwitch
```
python __main__.py -d XXX.XXX.XXX.XXX
```
1. 直接手動刪除 flow , ip為 XXX.XXX.XXX.XXX 到 OpenDaylight
2. OpenDaylight 會再透過自己的通訊協定給OpenVSwitch
```
python __main__.py -D
```
1. POST FlowTable 的要求給 OpenDaylight
2. OpenDaylight 會再透過自己的通訊協定給OpenVSwitch

```
python __main__.py -D
```
1. GET FlowTable 的要求給 OpenDaylight
2. 顯示所有在 OpenVswithc 上的 Flow 有哪些


## Snort_reptile.py
主要用於監聽Snort接收到alert時產生出.log的資料夾  
如果資料夾有更動了會傳送給連接Snort的Client  

