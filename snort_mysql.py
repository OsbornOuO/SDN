import pymysql
import pymysql.cursors
from odl_send import odl_send_instruction

class ip:
    table = dict()

def mysql_select (sql_instruction):
    connection=pymysql.connect(host='140.126.130.42',
                               user='root',
                               password='snort',
                               db='snort',
                               port=3306,
                               charset='utf8')
    try:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(sql_instruction)
            results = cursor.fetchall()
            for row in results:
                if row[0] in ip.table.keys():
                    print("IP %16s 已經在 Flow 內"%(str(row[0])))
                else:
                    odl_send_instruction(row[0])
                    ip.table.setdefault(row[0])
            connection.commit()
    finally:
        connection.close()