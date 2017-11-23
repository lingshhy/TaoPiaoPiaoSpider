import re
import traceback
import pymysql

class TppDB:
    def __init__(self):
        self.conn = None

    # 连接数据库
    def connect(self):
        self.conn = pymysql.connect("localhost", "root", "0000", "TaoPiaoPiaoDB", use_unicode=True, charset="utf8")

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    # 查看表是否存在
    def is_exist_table(self, table_name):
        sql = """SELECT table_name FROM information_schema.TABLES WHERE table_name = %s;"""
        cursor = self.conn.cursor()
        res = cursor.execute(sql, table_name)
        cursor.close()
        return res

    # 创建电影列表
    def create_table_movies_list(self):
        # 如果存在该表，则无需创建
        if self.is_exist_table("movieslist") == 1:
            return

        sql = """CREATE TABLE If Not Exists movieslist (
                ID INT AUTO_INCREMENT,
                NAME NVARCHAR(50) NOT NULL,
                TABLENAME NVARCHAR(50) NOT NULL,
                HREF NVARCHAR(255) NOT NULL,
                HASTABLE INT NOT NULL,
                PRIMARY KEY (ID)
                )AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
        except:
            self.conn.rollback()
            print(traceback.print_exc())

    # 更新电影列表
    def update_movies_list(self, movie_name, table_name, movie_href):
        select_sql = """SELECT * FROM movieslist WHERE NAME=%s"""
        insert_sql = """INSERT INTO movieslist (NAME, TABLENAME, HREF, HASTABLE) VALUES (%s, %s, %s, 0)"""
        try:
            cursor = self.conn.cursor()
            #  查询是否已存该电影
            line = 0
            line = cursor.execute(select_sql, movie_name)
            if line == 0:
                cursor.execute(insert_sql , (movie_name, table_name, movie_href))
            cursor.close()
        except:
            self.conn.rollback()
            print(traceback.print_exc())

    #  查找该电影对应的表名和链接
    def get_table_href(self, movie_name):
        select_sql = """SELECT TABLENAME,HREF FROM movieslist WHERE NAME=%s"""
        cursor = self.conn.cursor()
        cursor.execute(select_sql , movie_name)
        res = cursor.fetchone()
        cursor.close()
        return res

    # 查找数据库中的电影列表
    def get_movie_table_name(self):
        select_sql = """SELECT NAME FROM movieslist WHERE HASTABLE=1"""
        cursor = self.conn.cursor()
        cursor.execute(select_sql)
        res = cursor.fetchall()
        cursor.close()
        return res

    # 查找数据
    def get_data(self, table_name):
        select_sql = """SELECT * FROM %s"""
        cursor = self.conn.cursor()
        cursor.execute(select_sql % table_name)
        res = cursor.fetchall()
        cursor.close()
        return res

    # 创建电影上映信息表
    def create_movie_table(self, movie_name, table_name):
        # 如果存在该表，则无需创建
        if self.is_exist_table(table_name) == 1:
            return

        #  建表语句
        create_sql = """CREATE TABLE If Not Exists %s (
                ID INT AUTO_INCREMENT,
                CINEMA_NAME NVARCHAR(50) NOT NULL,
                ONDATE DATE NOT NULL,
                ONTIME  TIME NOT NULL,
                TYPE NVARCHAR(20), 
                MALL_NAME NVARCHAR(50),
                SEAT_STATUS NVARCHAR(20),
                PRICE FLOAT,
                PRIMARY KEY (ID)
                )AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        # 将电影标记为已建表
        update_sql = """UPDATE movieslist SET HASTABLE=1 WHERE NAME = %s"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_sql % table_name)
            cursor.execute(update_sql, movie_name)
            cursor.close()
            self.conn.commit()
        except:
            self.conn.rollback()
            print(traceback.print_exc())

    # 插入电影上映信息
    def save_datas(self, table_name, results):
        insert_sql = """INSERT INTO %s (CINEMA_NAME, ONDATE, ONTIME, TYPE, MALL_NAME, SEAT_STATUS, PRICE)""" % table_name
        insert_sql += """ VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        s1 = re.findall(r"\d+\.?\d*", results[1])
        s2 = re.findall(r"\d+\.?\d*", results[2])
        results[1] = '2017' + '-' + s1[0] + '-' + s1[1]
        results[2] = s2[0] + ':' + s2[1] + ':' + '00'
        try:
            cursor = self.conn.cursor()
            cursor.execute(insert_sql, results)
            cursor.close()
            self.commit()
        except:
            print(results)
            self.conn.rollback()
            print(traceback.print_exc())

# sql = TppDB()
# sql.connect()
# sql.create_table_movies_list()
# sql.update_movies_list('羞羞的铁拳',"羞羞的铁拳表","111")
# sql.create_table_movie("羞羞的铁拳")
# sql.save_datas("羞羞的铁拳表", ["a","11月21日","19:20","b","c","d","2.0"])
# sql.commit()
# sql.close()