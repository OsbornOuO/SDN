import pymysql
import pymysql.cursors
import odl_send

def mysql_select (sql_instruction,ip_Table):
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
                if row[0] in ip_Table.keys():
                    print("IP %16s 已經在 Flow 內"%(str(row[0])))
                else:
                    ip_Table.setdefault(row[0])
                    odl_send.Instruction(row[0])
            connection.commit()
    finally:
        connection.close()