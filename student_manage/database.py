import pymysql
import app_config as cf


class Mysqls(object):
    def __init__(self):
        # 读取配置文件
        self.connect(cf.db)

    def connect(self, db):
        self.conn = pymysql.connect(
            host=db["host"], port=db["port"], user=db["user"], password=db["pass"], database=db["database"])  # 可以把主机连接等写入配置文件 等
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 获取所以数据
    def get_all(self, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    # 获取一行数据
    def get_one(self, sql, *args):
        self.cursor.execute(sql, args)
        res = self.cursor.fetchone()
        return res

    # 删除数据
    def remove(self, sql):
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交修改
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            # 发生错误时回滚
            self.conn.rollback()
            return False

    # 添加  就是添加一次提交多次
    def add_one(self, sql, *args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    # 添加并且带返回值
    def update(self, sql, *args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def get_close(self):
        self.cursor.close()
        self.conn.close()
