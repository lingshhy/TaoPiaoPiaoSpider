import pymysql


#CREATE DATABASE TaoPiaoPiaoDB DEFAULT CHARSET UTF8 COLLATE utf8_general_ci;
#GRANT ALL ON TaoPiaoPiaoDB.* TO testuser;

sql = """CREATE TABLE xiuxiudetiequan (
        ID INT AUTO_INCREMENT,
        CINEMA_NAME CHAR(50) NOT NULL,
        ONDATE CHAR(20) NOT NULL,
        ONTIME  CHAR(20) NOT NULL,
        TYPE CHAR(20), 
        MALL_NAME CHAR(50),
        SEAT_STATUS CHAR(20),
        PRICE FLOAT,
        PRIMARY KEY (ID)
        )AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;"""



db = pymysql.connect("localhost","testuser","test123","TaoPiaoPiaoDB" )
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS xiuxiudetiequan")
cursor.execute(sql)
cursor.execute("SHOW TABLES;")

data = cursor.fetchall()
for i in data:
    print(data)
db.close()