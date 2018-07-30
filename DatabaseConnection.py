# -*-coding:utf-8-*-
import pymysql
from datetime import datetime

# mysql -h sh-cdb-hpgxwiuk.sql.tencentcdb.com -P 62958 -u root -p
local_host = "localhost"
remote_host = "sh-cdb-hpgxwiuk.sql.tencentcdb.com"

class Connection(object):
    def connect_database(self):
        self.connection = pymysql.connect(host=remote_host,
                                          user='root',
                                          db='lovediarydb',
                                          passwd='wangpeisheng17',
                                          port=62958,
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

def exec_delete_account(accountid):
    database.connect_database()
    sql = "DELETE FROM account WHERE account_id='%d'"
    database.exec_update(sql % accountid)
    database.disconnect_database()

def exec_fetch_all_accounts():
    database.connect_database()
    sql = "SELECT * FROM account"
    database.exec_query(sql)
    accounts = database.fetch_cursor()
    database.disconnect_database()
    account_list = []
    for account in accounts:
        account_id, account_description, account_cost, account_spenderid, account_date, account_time, account_typeid = account
        account_list.append((account_id, account_date, account_time, account_description, account_cost, account_spenderid, account_typeid))
    return account_list

# if __name__ == "__main__":
    # exec_add_account("1", "2", "1", "1997-07-04", "17:30:25", "2")