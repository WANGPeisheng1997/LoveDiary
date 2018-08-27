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


def exec_add_spender(name):
    sql = "INSERT INTO spender(spender_name) " \
          "VALUES('%s')"
    database.exec_update(sql % name)


# def exec_change_spender_name(spender_id, new_name):


def exec_add_account(description, cost, spenderid, date, time, typeid):
    sql = "INSERT INTO account(account_description, account_cost, account_spenderid, account_date, account_time, account_typeid) " \
          "VALUES('%s','%s','%s','%s','%s','%s')"
    data = (description, cost, spenderid, date, time, typeid)
    database.exec_update(sql % data)


def exec_edit_account(description, cost, spenderid, date, time, typeid, accountid):
    sql = "UPDATE account " \
          "SET account_description='%s', account_cost='%s', account_spenderid='%s', account_date='%s', account_time='%s', account_typeid='%s'" \
          "WHERE account_id='%d'"
    print(sql)
    data = (description, cost, spenderid, date, time, typeid, accountid)
    database.exec_update(sql % data)


def exec_edit_account_column(column, value, accountid):
    sql = "UPDATE account " \
          "SET %s='%s' " \
          "WHERE account_id='%d'"
    data = (column, value, accountid)
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


def exec_fetch_all_spenders():
    sql = "SELECT * FROM spender"
    database.exec_query(sql)
    spender_list = database.fetch_cursor()
    return spender_list


def exec_fetch_user_with_id(id):
    sql = "SELECT * FROM users WHERE user_id='%d'"
    database.exec_query(sql % id)
    user = database.fetch_cursor()
    if len(user) == 0:
        return None
    else:
        return user[0]


def exec_user_login(username, password):
    sql = "SELECT user_id, user_permission FROM users WHERE user_name='%s' AND user_password='%s'"
    database.exec_query(sql % (username, password))
    user = database.fetch_cursor()
    if len(user) == 0:
        return None
    else:
        return user[0][0], user[0][1]

# database.connect_database()
# print(exec_user_login("wps","wps"))
# database.disconnect_database()

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
