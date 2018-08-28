# -*-coding:utf-8-*-
import pymysql
import dbconfig

exchange_rate = 16.31

class JapanConnection(object):
    def connect_database(self):
        self.connection = pymysql.connect(host=dbconfig.host,
                                          user=dbconfig.user,
                                          db="japantest",
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


japan_database = JapanConnection()


def exec_add_account(description, currency, cost, spenderid, date, time, typeid):
    sql = "INSERT INTO account(account_description, account_currency, account_cost, account_spenderid, account_date, account_time, account_typeid) " \
          "VALUES('%s','%s','%s','%s','%s','%s','%s')"
    data = (description, currency, cost, spenderid, date, time, typeid)
    japan_database.exec_update(sql % data)


def exec_delete_account(accountid):
    sql = "DELETE FROM account WHERE account_id='%d'"
    japan_database.exec_update(sql % accountid)


def exec_edit_account_column(column, value, accountid):
    sql = "UPDATE account " \
          "SET %s='%s' " \
          "WHERE account_id='%d'"
    data = (column, value, accountid)
    japan_database.exec_update(sql % data)


def exec_fetch_all_accounts():
    sql = "SELECT account_id, account_date, account_time, account_description, account_currency, account_cost, spender_name, type_name " \
          "FROM account, spender, account_type " \
          "WHERE account.account_spenderid=spender.spender_id AND account.account_typeid=account_type.type_id"
    japan_database.exec_query(sql)
    accounts = japan_database.fetch_cursor()
    return accounts


def exec_calculate_sum_for_each_type():
    sql = "SELECT account_type.type_name, account.account_currency, SUM(account.account_cost) " \
          "FROM account, account_type " \
          "WHERE account.account_typeid=account_type.type_id " \
          "GROUP BY account.account_typeid, account.account_currency"
    japan_database.exec_query(sql)
    sum = japan_database.fetch_cursor()
    return sum


def exec_calculate_sum_for_each_date():
    sql = "SELECT account_date, account_currency, SUM(account_cost) " \
          "FROM account " \
          "GROUP BY account_date, account_currency"
    japan_database.exec_query(sql)
    sum = japan_database.fetch_cursor()
    return sum


def exec_calculate_sum_for_each_person():
    sql = "SELECT spender.spender_name, account.account_currency, SUM(account.account_cost) " \
          "FROM account, spender " \
          "WHERE account.account_spenderid=spender.spender_id " \
          "GROUP BY account.account_spenderid, account.account_currency"
    japan_database.exec_query(sql)
    sum = japan_database.fetch_cursor()
    return sum


def exec_calculate_sum_for_specific_date_region_and_currency(date_control, currency):
    sql = "SELECT SUM(account_cost) " \
          "FROM account " \
          "WHERE account_currency = '%s' AND account_date " + date_control
    japan_database.exec_query(sql % currency)
    sum = japan_database.fetch_cursor()[0][0]
    if sum is None:
        return 0
    return sum


def exec_fetch_all_types():
    sql = "SELECT * FROM account_type"
    japan_database.exec_query(sql)
    type_list = japan_database.fetch_cursor()
    return type_list


def exec_fetch_all_spenders():
    sql = "SELECT * FROM spender"
    japan_database.exec_query(sql)
    spender_list = japan_database.fetch_cursor()
    return spender_list
