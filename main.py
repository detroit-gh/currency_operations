import requests
from flask import Flask, render_template


app = Flask(__name__)


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


@app.route('/')
def index():
    return 'Hello! Its my new homework task.'


@app.route('/eur_to_usd/<int:amount>/')
def eur_to_usd(amount):
    return get_course('USD', amount)


@app.route('/eur_to_gbp/<int:amount>/')
def eur_to_gbp(amount):
    return get_course('GBP', amount)


@app.route('/eur_to_php/<int:amount>/')
def eur_to_php(amount):
    return get_course('PHP', amount)


@app.route('/history/')
def get_history():
    with open('history.txt') as h:
        read_hist = h.readlines()
    return render_template('history_template.html', hist=read_hist)


if __name__ == '__main__':
    app.run()