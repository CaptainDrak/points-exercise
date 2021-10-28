from flask import Flask, request, jsonify
import request_logic as rl

app = Flask(__name__)

transactions = []

@app.route('/add', methods=['POST'])
def add():
    json = request.get_json()

    negative_check = rl.check_for_negative_balance(transactions, json)
    if negative_check[0] == False:
        transactions.append(request.get_json())
        return f'Transaction added:\n{transactions[-1]}'
    else: 
        return f'Payer total cannot be negative.\nCurrent payer total is {negative_check[1]}.', 400

@app.route('/spend', methods=['POST'])
def spend():
    json = request.get_json(cache=True)
    points = json['points']
    sorted_transactions = sorted(transactions, key=lambda d: d['timestamp'])
    total_balance = rl.calculate_total_balance(sorted_transactions)

    if total_balance < points:
        return f'Requested {points} points be spent, but there are only {total_balance} points available. Cannot request to spend more points than are available.', 400
    else:
        transactions.clear()
        new_transactions = rl.spend_points(sorted_transactions, points)
        for i in new_transactions:
            transactions.append(i)
        return f'{points} points spent successfully.'
    

@app.route('/balance')
def get():
    return rl.calculate_balances(transactions)