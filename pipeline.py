import pymysql
import traceback

def saveDatas(db, cursor, results):
    insert_sql= """INSERT INTO xiuxiudetiequan(CINEMA_NAME, ONDATE, ONTIME, TYPE, MALL_NAME, SEAT_STATUS, PRICE)
                  VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    try:
        cursor.execute(insert_sql,results)
        db.commit()
    except:
        db.rollback()
        print('插入数据错误')
        print(traceback.print_exc())

# db = pymysql.connect("localhost","testuser","test123","TaoPiaoPiaoDB", use_unicode=True, charset="utf8")
# cursor = db.cursor()
# s=('哈艺时尚影城（白云YH城店）', '10月20日（周五）', '23:25', '英语 3D', '1号巨幕全景声厅', '宽松', '29.00')
# # saveDatas(db, cursor, s)
# print('('+s[1].strip()+')')


# db = pymysql.connect("localhost","testuser","test123","TaoPiaoPiaoDB", use_unicode=True, charset="utf8")
# cursor = db.cursor()

# saveDatas(db, cursor, results=s)
# cursor.execute("SELECT * FROM xiuxiudetiequan")
# data = cursor.fetchall()
# for i in data:
#     print(i)
# db.close()