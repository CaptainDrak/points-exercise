from flask import Flask, request, jsonify

app = Flask(__name__)

transactions = []
balance = {}

@app.route('/add', methods=['POST'])
def add_transaction():
    transactions.append(request.get_json())
    return f'Transaction added:\n{transactions[-1]}'

@app.route('/spend', methods=['POST'])
#def spend_points():
#    sorted_transactions = sorted(transactions, key=lambda d: d['timestamp'])
#    return jsonify(sorted_transactions)

@app.route('/balance')
def get_balance():
    for i in transactions:
        if i['payer'] in balance.keys():
            balance[i['payer']] = balance[i['payer']] + i['points']
        elif i['payer'] not in balance.keys():
            balance[i['payer']] = i['points']
    return balance