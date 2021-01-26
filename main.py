import requests
from flask import Flask


app = Flask(__name__)


def get_course(currency):
    response = requests.get('https://api.exchangeratesapi.io/latest')
    response_json = response.json()
    rates = response_json['rates']
    return rates[currency]


@app.route('/')
def index():
    return 'Hello! Its my new homework task.'


@app.route('/eur_to_usd/<int:amount>/')
def eur_to_usd(amount):
    course = get_course("USD")
    euro = course * amount
    with open("history.html", "a") as h:
        h.write(f'<p>USD,{course},{amount},{euro}</p>')
    return str(euro)


@app.route('/eur_to_gbp/<int:amount>/')
def eur_to_gbp(amount):
    course = get_course("GBP")
    euro = course * amount
    with open("history.html", "a") as h:
        h.write(f'<p>GBP,{course},{amount},{euro}</p>')
    return str(euro)


@app.route('/eur_to_php/<int:amount>/')
def eur_to_php(amount):
    course = get_course("PHP")
    euro = course * amount
    with open("history.html", "a") as h:
        h.write(f'<p>PHP,{course},{amount},{euro}</p>')
    return str(euro)


@app.route('/history/')
def get_history():
    with open('history.html', 'r') as h:
        read_hist = h.read()
    return read_hist


if __name__ == '__main__':
    open('history.html', 'tw')
    app.run()