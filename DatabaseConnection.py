# -*-coding:utf-8-*-
import pymysql
import dbconfig


class Connection(object):
    def connect_database(self):
        self.connection = pymysql.connect(host=dbconfig.host,
                                          user=dbconfig.user,
                                          db=dbconfig.db,
                                          passwd=dbconfig.passwd,
                                          port=dbconfig.port,
                                          charset=dbconfig.charset
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
    sql = "INSERT INTO account(account_description, account_cost, account_spenderid, account_date, account_time, account_typeid) " \
          "VALUES('%s','%s','%s','%s','%s','%s')"
    data = (description, cost, spenderid, date, time, typeid)
    database.exec_update(sql % data)


def exec_delete_account(accountid):
    sql = "DELETE FROM account WHERE account_id='%d'"
    database.exec_update(sql % accountid)


def exec_fetch_all_accounts():
    sql = "SELECT account_id, account_date, account_time, account_description, account_cost, spender_name, type_name " \
          "FROM account, spender, account_type " \
          "WHERE account.account_spenderid=spender.spender_id AND account.account_typeid=account_type.type_id"
    database.exec_query(sql)
    accounts = database.fetch_cursor()
    return accounts


def exec_fetch_all_types():
    sql = "SELECT * FROM account_type"
    database.exec_query(sql)
    type_list = database.fetch_cursor()
    return type_list


# def exec_query_spender_from_id(spender_id):
#     start = time.clock()
#     # database.connect_database()
#     sql = "SELECT spender_name FROM spender WHERE spender_id='%d'"
#     database.exec_query(sql % spender_id)
#     spender_name = database.fetch_cursor()[0][0]
#     # database.disconnect_database()
#
#     end = time.clock()
#     print(end - start)
#     return spender_name
#
#
# def exec_query_type_from_id(type_id):
#     # database.connect_database()
#     sql = "SELECT type_name FROM account_type WHERE type_id='%d'"
#     database.exec_query(sql % type_id)
#     type_name = database.fetch_cursor()[0][0]
#     # database.disconnect_database()
#     return type_name

# if __name__ == "__main__":
    # exec_add_account("1", "2", "1", "1997-07-04", "17:30:25", "2")
