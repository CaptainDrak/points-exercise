#calculates existing balances for all payers
#accepts a list of transactions
#returns a list of balances for each payer
def calculate_balances(transactions):
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
def calculate_total_balance(transactions):
    total_balance = 0
    for i in transactions:
        total_balance += i['points']
    return total_balance


#checks for potential negative values for payer totals
#accepts a list of transactions and a transaction request
#returns True/False and point total integer for that payer
def check_for_negative_balance(transactions, request):
    point_balances = calculate_balances(transactions)
    if request['payer'] not in point_balances.keys() and request['points'] >= 0:
        return False, 0
    elif request['payer'] not in point_balances.keys() and request['points'] < 0:
        return True, 0
    elif request['payer'] in point_balances.keys():
        if (point_balances[request['payer']] + request['points']) < 0:
            return True, point_balances[request['payer']]
        else: return False, point_balances[request['payer']]

#spends a requested total of points
#accepts a list of transactions and a points integer
#returns a list of transations
def spend_points(sorted_transactions, points):
    counter = 0
    while points > 0:
        for i in sorted_transactions:
            if (points - i['points']) > 0:
                points = points - i['points']
                i['points'] = 0
                counter+=1
            elif (points - i['points']) == 0:
                i['points'] = 0
                del sorted_transactions[0:counter]
                points = 0
                del sorted_transactions[0:counter]
                break
            elif (points - i['points']) < 0:
                i['points'] = i['points'] - points
                del sorted_transactions[0:counter]
                points = 0
                break
    return sorted_transactions