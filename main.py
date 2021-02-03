import requests
import sqlite3
from flask import Flask, request, render_template
from flask import g

app = Flask(__name__)

DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        conn = sqlite3.connect(DATABASE)
        db = g._database = conn
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_course(currency, amount):
    response = requests.get('https://api.exchangeratesapi.io/latest')
    response_json = response.json()
    rates = response_json['rates']
    value = rates[currency] * amount
    get_log(currency, rates, amount, value)
    return str(value)


def get_log(currency, rates, amount, value):
    with open("history.txt", "a") as h:
        h.write(f'{currency},{rates[currency]},{amount},{value}\n')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        insert into exchange ('currency_to', 'exchange_rate', 'amount', 'result')
        values (?, ?, ?, ?)
        """, (str.lower(currency), rates[currency], amount, value)
    )
    conn.commit()


@app.route('/')
def index():
    return 'Hello! Its my new homework task.'


@app.route('/eur_to_usd/<int:amount>/')
def eur_to_usd(amount):
    return get_course('USD', amount)


@app.route('/eur_to_gbp/<int:amount>/')
def eur_to_gbp(amount):
    return get_course(str('GBP'), amount)


@app.route('/eur_to_php/<int:amount>/')
def eur_to_php(amount):
    return get_course('PHP', amount)


@app.route('/history/')
def get_history():
    with open('history.txt') as h:
        read_hist = h.readlines()
    return render_template('history_template.html', hist=read_hist)


@app.route('/history/currency/<to_currency>/')
def get_curr_hist(to_currency):
    conn = get_db()
    cursor = conn.cursor()
    resp = cursor.execute("""
        select currency_to, exchange_rate, amount, result
        from exchange
        where currency_to = ?
        """, (to_currency, ))
    resp = cursor.fetchall()
    return render_template('history_template.html', hist=resp)


@app.route('/history/amount_gte/<int:number>')
def get_numb_hist(number):
    conn = get_db()
    cursor = conn.cursor()
    resp = cursor.execute("""
        select currency_to, exchange_rate, amount, result
        from exchange
        where amount >= ?
        """, (number, ))
    resp = cursor.fetchall()
    return render_template('history_template.html', hist=resp)


@app.route('/history/statistic/')
def get_stat_hist():
    conn = get_db()
    cursor = conn.cursor()
    resp = cursor.execute("""
        select currency_to, count(*), sum(result)
        from exchange
        group by currency_to
        """)
    resp = cursor.fetchall()
    return render_template('history_template.html', hist=resp)


if __name__ == '__main__':
    init_db()
    app.run()