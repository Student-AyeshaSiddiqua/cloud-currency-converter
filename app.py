from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your own API key from exchangerate-api.com
import os
API_KEY = os.environ.get('API_KEY')  # Securely load from environment
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

@app.route('/', methods=['GET', 'POST'])
def index():
    converted_amount = None
    currencies = []

    if request.method == 'POST':
        from_currency = request.form['from']
        to_currency = request.form['to']
        amount = float(request.form['amount'])

        response = requests.get(API_URL + from_currency)
        data = response.json()

        if data['result'] == 'success':
            rate = data['conversion_rates'][to_currency]
            converted_amount = round(amount * rate, 2)
            currencies = list(data['conversion_rates'].keys())

    # Default list on first GET
    if not currencies:
        response = requests.get(API_URL + "USD")
        data = response.json()
        currencies = list(data['conversion_rates'].keys())

    return render_template('index.html', converted_amount=converted_amount, currencies=currencies)

if __name__ == '__main__':
    app.run(debug=True)
