import pymysql
import pymysql.cursors
import odl_send

def mysql_select (option,sql_instruction,flow):
    connection=pymysql.connect(host='140.126.130.42',
                               user='root',
                               password='snort',
                               db='snort',
                               port=3306,
                               charset='utf8')
    try:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            try:
                cursor.execute(sql_instruction)
            except ValueError:
                print("MySQL 無此IP")
            results = cursor.fetchall()
            if option == 0:
                for row in results:
                    if row[0] in flow.ip:
                        print("IP %16s 已經在 Flow 內" % (str(row[0])))
                    else:
                        flow.ip.append(row[0])
                        flow.id.append(flow.id_count)
                        odl_send.Instruction(flow.id_count,row[0])
                        flow.id_count+=1
            elif option == 1:
                odl_send.Delete_One(flow)
            connection.commit()
    finally:
        connection.close()
