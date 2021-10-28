from flask import Flask, request, jsonify
import request_logic as rl

app = Flask(__name__)

transactions = []

@app.route('/add', methods=['POST'])
def add_transaction():
    json = request.get_json()
    negative_check = rl.check_for_negative_balance(transactions, json)
    if negative_check[0] == False:
        transactions.append(request.get_json())
        return f'Transaction added:\n{transactions[-1]}'
    else: 
        return f'Payer total cannot be negative.\nCurrent payer total is {negative_check[1]}.', 400

@app.route('/spend', methods=['POST'])
def spend_points():
    sorted_transactions = sorted(transactions, key=lambda d: d['timestamp'])
    return jsonify(sorted_transactions)

@app.route('/balance')
def get_balance():
    return rl.calculate_balance(transactions)