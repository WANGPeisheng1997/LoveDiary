# -*-coding:utf-8-*-

import DatabaseConnection
import JapanDatabaseConnection
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from datetime import datetime
from user import User
import time

app = Flask(__name__)
app.secret_key = 'asfasfasfasqwerqwr'


# homepage direction
@app.route('/')
@login_required
def index():
    return redirect('/moneymanagement')

# login routes and methods
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        DatabaseConnection.database.connect_database()
        print(request.form)
        if "username" in request.form and "password" in request.form:
            username = request.form['username']
            password = request.form['password']
            userid = DatabaseConnection.exec_user_login(username, password)
            print(username, password, userid)
        else:
            userid = None
        if userid is not None:
            login_user(User(id=userid, username=username))
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Logged in failed.')
            return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# routes for japan
@app.route('/japan/accounting', methods=['GET'])
@login_required
def japan_accounting():
    JapanDatabaseConnection.japan_database.connect_database()
    accounts = JapanDatabaseConnection.exec_fetch_all_accounts()
    types = JapanDatabaseConnection.exec_fetch_all_types()
    spenders = JapanDatabaseConnection.exec_fetch_all_spenders()
    JapanDatabaseConnection.japan_database.disconnect_database()
    return render_template('japan_accounting.html', account_list=accounts, type_list=types, spender_list=spenders)


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
        typeid = request.form['type']
        JapanDatabaseConnection.exec_add_account(description, currency, cost, spenderid, date_web_to_sql(date), time_web_to_sql(time),
                                            typeid)

    if post_type == "delete":
        accountid = int(request.form['accountid'])
        JapanDatabaseConnection.exec_delete_account(accountid)
    JapanDatabaseConnection.japan_database.disconnect_database()
    return redirect('/japan/accounting')


@app.route('/japan/schedule', methods=['GET'])
@login_required
def japan_schedule():
    return render_template('japan_schedule.html')


@app.route('/japan/maps', methods=['GET'])
@login_required
def japan_maps():
    return render_template('japan_maps.html')


# routes for love diary
@app.route('/moneymanagement', methods=['GET'])
@login_required
def money_management():
    start = time.clock()
    flash("hello")
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
    # print(date_web_to_sql("7/16/2015"))
    # print(date_sql_to_web("2015-07-03"))
    # print(time_web_to_sql("7:03 PM"))
