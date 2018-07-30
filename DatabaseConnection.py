# -*-coding:utf-8-*-
import pymysql
from datetime import datetime

local_host = "localhost"
remote_host = "sh-cdb-hpgxwiuk.sql.tencentcdb.com:62958"

class Connection(object):
    def connect_database(self):
        self.connection = pymysql.connect(host=remote_host,
                                          user='root',
                                          db='lovediarytest',
                                          passwd='wangpeisheng17',
                                          port=3306,
                                          charset="utf8"
                                          )
        self.cursor = self.connection.cursor()

    def disconnect_database(self):
        self.cursor.close()
        self.connection.close()

    def exec_query(self, sql):
        self.cursor.execute(sql)

    def exec_update(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()

    def fetch_cursor(self):
        return self.cursor.fetchall()

database = Connection()

# add a new account:

def exec_add_account(description, cost, spenderid, date, time, typeid):
    database.connect_database()
    sql = "INSERT INTO account(account_description, account_cost, account_spenderid, account_date, account_time, account_typeid) VALUES('%s','%s','%s','%s','%s','%s')"
    data = (description, cost, spenderid, date, time, typeid)
    database.exec_update(sql % data)
    database.disconnect_database()

# if __name__ == "__main__":
    # exec_add_account("1", "2", "1", "1997-07-04", "17:30:25", "2")