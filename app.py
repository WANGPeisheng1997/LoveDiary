# -*-coding:utf-8-*-

import DatabaseConnection
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/moneymanagement')


@app.route('/moneymanagement', methods=['GET'])
def money_management():
    return render_template('moneymanagement.html')


@app.route('/moneymanagement', methods=['POST'])
def add_form():
    description = request.form['description']
    cost = request.form['cost']
    spenderid = request.form['spender']
    date = request.form['date']
    time = request.form['time']
    typeid = request.form['type']
    DatabaseConnection.exec_add_account(description, cost, spenderid, date_web_to_sql(date), time_web_to_sql(time), typeid)
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
    app.run(debug=True)
    # print(date_web_to_sql("7/16/2015"))
    # print(date_sql_to_web("2015-07-03"))
    # print(time_web_to_sql("7:03 PM"))