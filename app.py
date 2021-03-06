# -*-coding:utf-8-*-

import DatabaseConnection
import JapanDatabaseConnection
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
from user import User
import time

app = Flask(__name__)
app.secret_key = 'asfasfasfasqwerqwr'


# homepage direction
@app.route('/')
@login_required
def index():
    return redirect('/japan/dashboard')

# login routes and methods
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "/japan/login"

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if "username" in request.form and "password" in request.form:
            username = request.form['username']
            password = request.form['password']
            DatabaseConnection.database.connect_database()
            userid, userpermission = DatabaseConnection.exec_user_login(username, password)
            DatabaseConnection.database.disconnect_database()
        else:
            userid = None
        if userid is not None:
            if userpermission == 1:
                login_user(User(id=userid, username=username))
                flash('Logged in successfully.')
                return redirect(url_for('index'))
            else:
                flash('Permission denied.')
                return render_template('login.html')
        else:
            flash('Wrong username or password!')
            return render_template('login.html')


@app.route('/japan/login', methods=['GET', 'POST'])
def japan_login():
    if request.method == 'GET':
        return render_template('japan_login.html')
    if request.method == 'POST':
        if "username" in request.form and "password" in request.form:
            username = request.form['username']
            password = request.form['password']
            DatabaseConnection.database.connect_database()
            userid, userpermission = DatabaseConnection.exec_user_login(username, password)
            DatabaseConnection.database.disconnect_database()
        else:
            userid = None
        if userid is not None:
            login_user(User(id=userid, username=username))
            flash('Logged in successfully.')
            return redirect(url_for('japan_dashboard'))
        else:
            flash('Wrong username or password!')
            return redirect(url_for('japan_dashboard'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# routes for japan
@app.route('/japan/dashboard', methods=['GET'])
@login_required
def japan_dashboard():
    JapanDatabaseConnection.japan_database.connect_database()
    pie_data = []
    pie_labels = []
    pydata = JapanDatabaseConnection.exec_calculate_sum_for_each_type() # (type_name, currency, cost)
    rate = JapanDatabaseConnection.exchange_rate
    dict = {}
    for type_name, currency, sum in pydata:
        if type_name not in dict:
            dict[type_name] = 0
        if currency == "CNY":
            dict[type_name] = dict[type_name] + float(sum)
        else:
            dict[type_name] = dict[type_name] + float(sum) / rate
    for type_name in dict:
        pie_data.append('%.2f' % dict[type_name])
        pie_labels.append(type_name)

    cny = []
    jpy = []
    total = []
    date_controls = ["< '2018-08-29'", "= '2018-08-29'", "= '2018-08-30'", "= '2018-08-31'", "= '2018-09-01'",
                     "= '2018-09-02'", "= '2018-09-03'", "= '2018-09-04'", "> '2018-09-04'"]
    for date_control in date_controls:
        cnyt = float(JapanDatabaseConnection.exec_calculate_sum_for_specific_date_region_and_currency(date_control, 'CNY'))
        cny.append(cnyt)
        jpyt = float(JapanDatabaseConnection.exec_calculate_sum_for_specific_date_region_and_currency(date_control, 'JPY'))
        jpy.append('%.2f' % (jpyt / rate))
        total.append('%.2f' % (cnyt + jpyt / rate))

    JapanDatabaseConnection.japan_database.disconnect_database()
    return render_template('japan_dashboard.html', user=current_user.username, pie_data=pie_data, pie_labels=pie_labels, cnydata=cny, jpydata=jpy, totaldata=total)


@app.route('/japan/accounting', methods=['GET'])
@login_required
def japan_accounting():
    JapanDatabaseConnection.japan_database.connect_database()
    accounts = JapanDatabaseConnection.exec_fetch_all_accounts()
    types = JapanDatabaseConnection.exec_fetch_all_types()
    spenders = JapanDatabaseConnection.exec_fetch_all_spenders()
    JapanDatabaseConnection.japan_database.disconnect_database()
    return render_template('japan_accounting.html', user=current_user.username, account_list=accounts, type_list=types, spender_list=spenders)


@app.route('/japan/accounting/<post_type>', methods=['POST'])
@login_required
def japan_process_form_post(post_type=None):
    JapanDatabaseConnection.japan_database.connect_database()
    if post_type == "add":
        description = request.form['description']
        currency = request.form['currency']
        cost = request.form['cost']
        spenderid = request.form['spender']
        date = request.form['date']
        time = request.form['time']
        if time == '':
            formatted_time = ''
        else:
            formatted_time = time_web_to_sql(time)
        typeid = request.form['type']
        JapanDatabaseConnection.exec_add_account(description, currency, cost, spenderid, date_web_to_sql(date), time_web_to_sql(time),
                                            typeid)

    if post_type == "edit":
        accountid = int(request.form['accountid'])
        description = request.form['description']
        if description != '':
            JapanDatabaseConnection.exec_edit_account_column('account_description', description, accountid)

        if 'currency' in request.form:
            currency = request.form['currency']
            JapanDatabaseConnection.exec_edit_account_column('account_currency', currency, accountid)

        cost = request.form['cost']
        if cost != '':
            JapanDatabaseConnection.exec_edit_account_column('account_cost', cost, accountid)

        if 'spender' in request.form:
            spenderid = request.form['spender']
            JapanDatabaseConnection.exec_edit_account_column('account_spenderid', spenderid, accountid)

        date = request.form['date']
        if date != '':
            JapanDatabaseConnection.exec_edit_account_column('account_date', date_web_to_sql(date), accountid)

        time = request.form['time']
        if time != '':
            JapanDatabaseConnection.exec_edit_account_column('account_time', time_web_to_sql(time), accountid)

        typeid = request.form['type']
        if typeid != '':
            JapanDatabaseConnection.exec_edit_account_column('account_typeid', typeid, accountid)

    if post_type == "delete":
        accountid = int(request.form['accountid'])
        JapanDatabaseConnection.exec_delete_account(accountid)

    JapanDatabaseConnection.japan_database.disconnect_database()
    return redirect('/japan/accounting')


@app.route('/japan/statistics', methods=['GET'])
@login_required
def japan_statistics():
    JapanDatabaseConnection.japan_database.connect_database()
    cost_type_list = japan_stats_of_each_type()
    cost_date_list = japan_stats_of_each_date()
    cost_person_list = japan_stats_of_each_person()
    JapanDatabaseConnection.japan_database.disconnect_database()
    return render_template('japan_statistics.html', user=current_user.username, cost_type_list=cost_type_list, cost_date_list=cost_date_list, cost_person_list=cost_person_list)


def japan_stats_to_list(stats):
    rate = JapanDatabaseConnection.exchange_rate
    dict = {}
    for col, currency, sum in stats:
        if col not in dict:
            dict[col] = {"CNY": 0.0, "JPY": 0.0, "JPYex": 0.0, "total": 0.0}
        if currency == "CNY":
            dict[col]["CNY"] = dict[col]["CNY"] + float(sum)
            dict[col]["total"] = dict[col]["total"] + float(sum)
        else:
            dict[col]["JPY"] = dict[col]["JPY"] + float(sum)
            dict[col]["JPYex"] = dict[col]["JPYex"] + float(sum) / rate
            dict[col]["total"] = dict[col]["total"] + float(sum) / rate
    list = []
    for col in dict:
        record = [col, '%.2f' % dict[col]["CNY"], '%.2f' % dict[col]["JPY"],
                  '%.2f' % dict[col]["JPYex"], '%.2f' % dict[col]["total"]]
        list.append(record)
    return list


def japan_stats_of_each_type():
    stats = JapanDatabaseConnection.exec_calculate_sum_for_each_type()
    return japan_stats_to_list(stats)


def japan_stats_of_each_date():
    stats = JapanDatabaseConnection.exec_calculate_sum_for_each_date()
    return japan_stats_to_list(stats)


def japan_stats_of_each_person():
    stats = JapanDatabaseConnection.exec_calculate_sum_for_each_person()
    return japan_stats_to_list(stats)


@app.route('/japan/schedule', methods=['GET'])
@login_required
def japan_schedule():
    return render_template('japan_schedule.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    DatabaseConnection.database.connect_database()
    pie_data = []
    pie_labels = []
    pydata = DatabaseConnection.exec_calculate_sum_for_each_type()
    for type_name, sum in pydata:
        pie_data.append(float(sum))
        pie_labels.append(type_name)

    wps = []
    sweetie = []
    total = []
    months = ['2018-06', '2018-07', '2018-08']
    for month in months:
        wpst = float(DatabaseConnection.exec_calculate_sum_for_specific_month_and_spender(1, month))
        wps.append(wpst)
        sweetiet = float(DatabaseConnection.exec_calculate_sum_for_specific_month_and_spender(2, month))
        sweetie.append(sweetiet)
        total.append(wpst + sweetiet)
        print(wpst, sweetiet)

    print(pydata)
    DatabaseConnection.database.disconnect_database()
    return render_template('dashboard.html', pie_data=pie_data, pie_labels=pie_labels, wpsdata=wps, sweetiedata=sweetie, totaldata=total)


# routes for love diary
@app.route('/moneymanagement', methods=['GET'])
@login_required
def money_management():
    start = time.clock()
    DatabaseConnection.database.connect_database()
    accounts = DatabaseConnection.exec_fetch_all_accounts()
    types = DatabaseConnection.exec_fetch_all_types()
    spenders = DatabaseConnection.exec_fetch_all_spenders()
    DatabaseConnection.database.disconnect_database()
    end = time.clock()
    print("Load Time: " + str(end-start) + "s")
    return render_template('moneymanagement.html', account_list=accounts, type_list=types, spender_list=spenders)


@app.route('/moneymanagement/<post_type>', methods=['POST'])
@login_required
def process_form_post(post_type=None):
    DatabaseConnection.database.connect_database()
    if post_type == "add":
        description = request.form['description']
        cost = request.form['cost']
        spenderid = request.form['spender']
        date = request.form['date']
        time = request.form['time']
        if time == '':
            formatted_time = ''
        else:
            formatted_time = time_web_to_sql(time)
        typeid = request.form['type']
        DatabaseConnection.exec_add_account(description, cost, spenderid, date_web_to_sql(date), formatted_time,
                                            typeid)

    if post_type == "edit":
        accountid = int(request.form['accountid'])
        description = request.form['description']
        if description != '':
            DatabaseConnection.exec_edit_account_column('account_description', description, accountid)
        cost = request.form['cost']
        if cost != '':
            DatabaseConnection.exec_edit_account_column('account_cost', cost, accountid)

        if 'spender' in request.form:
            spenderid = request.form['spender']
            DatabaseConnection.exec_edit_account_column('account_spenderid', spenderid, accountid)

        date = request.form['date']
        if date != '':
            DatabaseConnection.exec_edit_account_column('account_date', date_web_to_sql(date), accountid)

        time = request.form['time']
        if time != '':
            DatabaseConnection.exec_edit_account_column('account_time', time_web_to_sql(time), accountid)

        typeid = request.form['type']
        if typeid != '':
            DatabaseConnection.exec_edit_account_column('account_typeid', typeid, accountid)

    if post_type == "delete":
        accountid = int(request.form['accountid'])
        DatabaseConnection.exec_delete_account(accountid)

    DatabaseConnection.database.disconnect_database()
    return redirect('/moneymanagement')


def date_web_to_sql(date):
    trans = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
    return trans


def date_sql_to_web(date):
    trans = datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
    return trans


def time_web_to_sql(date):
    trans = datetime.strptime(date, '%I:%M %p').strftime('%H:%M:%S')
    return trans


def time_sql_to_web(date):
    trans = datetime.strptime(date, '%H:%M:%S').strftime('%I:%M %p')
    return trans


if __name__ == '__main__':
    app.run(debug=True, host=('0.0.0.0'))
    #app.run(debug=True)
