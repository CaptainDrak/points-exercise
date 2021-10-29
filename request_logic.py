import request_json_validation as rj

transactions = []

#calculates existing balances for all payers
#accepts a list of transactions
#returns a list of balances for each payer
def calculate_balances():
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
def calculate_total_balance(passed_transactions):
    total_balance = 0
    for i in passed_transactions:
        total_balance += i['points']
    return total_balance


#checks for potential negative values for payer totals
#accepts a transaction request
#returns True/False and point total integer for that payer
def check_for_negative_balance(request):
    payer_point_balances = calculate_balances()
    if request['payer'] not in payer_point_balances.keys() and request['points'] >= 0:
        return False, 0
    elif request['payer'] not in payer_point_balances.keys() and request['points'] < 0:
        return True, 0
    elif request['payer'] in payer_point_balances.keys():
        if (payer_point_balances[request['payer']] + request['points']) < 0:
            return True, payer_point_balances[request['payer']]
        else: return False, payer_point_balances[request['payer']]

#spends a requested total of points
#accepts a list of transactions and a points integer
#returns a list of transations
def point_spender(passed_sorted_transactions, points):
    counter = 0
    while points > 0:
        for i in passed_sorted_transactions:
            if (points - i['points']) > 0:
                points = points - i['points']
                i['points'] = 0
                counter+=1
            elif (points - i['points']) == 0:
                i['points'] = 0
                del passed_sorted_transactions[0:counter+1]
                points = 0
                break
            elif (points - i['points']) < 0:
                i['points'] = i['points'] - points
                del passed_sorted_transactions[0:counter]
                points = 0
                break
    return passed_sorted_transactions

#carries out collective logic required for add endpoint
#accepts a request
#returns an error if one is thrown, or a successful point addition response
def add_points(add_request):
    json_validation = rj.add_json_validation(add_request)

    if json_validation != None:
        return json_validation, 400

    negative_check = check_for_negative_balance(add_request)
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
    
    points = spend_request['points']
    sorted_transactions = sorted(transactions, key=lambda d: d['timestamp'])
    total_balance = calculate_total_balance(sorted_transactions)
    json_validation = rj.spend_json_validation(spend_request)

    if total_balance < points:
        return f'Requested {points} points be spent, but there are only {total_balance} points available. Cannot request to spend more points than are available.', 400
    else:
        transactions.clear()
        new_transactions = point_spender(sorted_transactions, points)
        for i in new_transactions:
            transactions.append(i)
        return f'{points} points spent successfully.'
