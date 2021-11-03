import request_json_validation as rj
from flask import jsonify

transactions = []

#sorts transactions by timestamp
def sort_transactions():
    sorted_transactions = sorted(transactions, key=lambda d: d['timestamp'])
    
    transactions.clear()

    for i in sorted_transactions:
        transactions.append(i)


#calculates existing balances for all payers and trims zero-sum balances
#accepts a list of transactions
#returns a dict of balances by payer
def calculate_balances():
    sort_transactions()
    point_balances = {}
    for i in transactions:
        if i['payer'] in point_balances.keys():
            point_balances[i['payer']] = point_balances[i['payer']] + i['points']
        else:
            point_balances[i['payer']] = i['points']
    return point_balances


#calculates total point balance across all payers
#accepts a list of transactions
#returns a point total integer
def calculate_total_balance():
    total_balance = 0
    for i in transactions:
        total_balance += i['points']
    return total_balance


#calculates total balance spent, based on differences in passed balances
#accepts two dicts of balances by payer (identical to returned value of calculate_balances())
#returns a jsonified dict of spent balances by payer
def calculate_spent_balances(original_balance, new_balance):
    spent_points = {}
    spent_points_list = []
    for i in original_balance:
        if i not in new_balance:
            spent_points[i] = 0 - original_balance[i]
        elif i in new_balance and original_balance[i] != new_balance[i]:
            spent_points[i] = new_balance[i] - original_balance[i]
    for i in spent_points:
        spent_points_list.append({"payer": i, "points": spent_points[i]})
    response = jsonify(spent_points_list)
    return response


#checks for potential negative values for payer totals
#accepts a transaction request
#returns True/False and point total integer for that payer
def check_for_negative_balance_on_request(request):
    payer_point_balances = calculate_balances()
    if request['payer'] not in payer_point_balances.keys() and request['points'] >= 0:
        return False, 0
    elif request['payer'] not in payer_point_balances.keys() and request['points'] < 0:
        return True, 0
    elif request['payer'] in payer_point_balances.keys():
        if (payer_point_balances[request['payer']] + request['points']) < 0:
            return True, payer_point_balances[request['payer']]
        else: return False, payer_point_balances[request['payer']]


#checks for any payers with a negative point balance
#returns an amount of points past what they were able to spend integer
def check_for_delinquent_payer():
    delinquent_points = 0
    current_balance = calculate_balances()
    for i in current_balance:
        if current_balance[i] < 0:
            delinquent_points -= current_balance[i]
            delinquent_payer = i
            counter_3 = 0
            for t in transactions:
                if t['payer'] == delinquent_payer:
                    transactions[counter_3]['points'] = 0
                counter_3 += 1
    return delinquent_points


#spends a requested number of points
#accepts a points integer
def point_spender(points):
    sort_transactions()
    counter = 0
    while points > 0:
        for i in transactions:
            if (points - i['points']) > 0:
                points = points - i['points']
                i['points'] = 0
                counter+=1
            elif (points - i['points']) == 0:
                i['points'] = 0
                points = check_for_delinquent_payer()
                break
            elif (points - i['points']) < 0:
                i['points'] = i['points'] - points
                points = check_for_delinquent_payer()
                break


#carries out collective logic required for add endpoint
#accepts a request
#returns an error if one is thrown, or a successful point addition response
def add_points(add_request):
    json_validation = rj.add_json_validation(add_request)

    if json_validation != None:
        return json_validation, 400

    negative_check = check_for_negative_balance_on_request(add_request)

    if negative_check[0] == False:
        transactions.append(add_request)
        return f'Transaction added:\n{transactions[-1]}'
    else: 
        return f'Payer total cannot be negative.\nCurrent payer total is {negative_check[1]}.', 400


#carries out collective logic required for spend endpoint
#accepts a request
#returns an error if one is thrown, or a successful point spending response
def spend_points(spend_request):
    json_validation = rj.spend_json_validation(spend_request)

    if json_validation != None:
        return json_validation, 400
    
    original_balance = calculate_balances()
    points = spend_request['points']
    total_balance = calculate_total_balance()
    json_validation = rj.spend_json_validation(spend_request)

    if points <= 0:
        return f'Must request a positive, non-negative amount of points to spend.', 400
    if total_balance < points:
        return f'Requested {points} points be spent, but there are only {total_balance} points available. Cannot request to spend more points than are available.', 400
    else:
        point_spender(points)
        new_balance = calculate_balances()
        return calculate_spent_balances(original_balance, new_balance)
