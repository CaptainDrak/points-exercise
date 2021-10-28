def calculate_balance(transactions):
    balance = {}
    for i in transactions:
        if i['payer'] in balance.keys():
            balance[i['payer']] = balance[i['payer']] + i['points']
        else:
            balance[i['payer']] = i['points']
    return balance

def check_for_negative_balance(transactions, request):
    balance = calculate_balance(transactions)
    if request['payer'] not in balance.keys() and request['points'] >= 0:
        return False, 0
    elif request['payer'] not in balance.keys() and request['points'] < 0:
        return True, 0
    elif request['payer'] in balance.keys():
        if (balance[request['payer']] + request['points']) < 0:
            return True, balance[request['payer']]
        else: return False, balance[request['payer']]
