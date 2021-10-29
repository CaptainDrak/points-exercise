from flask import Flask, request
import request_logic as rl

app = Flask(__name__)

transactions = []

#route through which points are added for a specific payer
@app.route('/add', methods=['POST'])
def add():
    return rl.add_points(request.get_json(cache=True))

#route through which a requested amount of points is spent
@app.route('/spend', methods=['POST'])
def spend():
    return rl.spend_points(request.get_json(cache=True))
    
#route through which a request for all point balances by payer is fulfilled
@app.route('/balance')
def get():
    return rl.calculate_balances()