from flask import Flask, request, jsonify, render_template
from pulp import *
import json
app = Flask(__name__)


def reprocess_input(data):
    offers = data['offers']
    customers = data['customers']
    matrix = data['matrix']
    conflicts = data['constraints']['conflicts']

    #We want to index by customer and offer. Like `dm[customer][offer]`
    dm = {}
    for i in range(len(matrix)):
        dic = {}
        for j in range(len(matrix[i])):
            dic[offers[j]] = matrix[i][j]
        dm[customers[i]] = dic

    data['dm'] = dm

    cs = {}
    for offer in offers:
        cs[offer] = set([])

    #Avoid duplicities by lexicographic ordering
    for pair in conflicts:
        if pair[0] > pair[1]:
            cs[pair[0]].add(pair[1])
        else:
            cs[pair[1]].add(pair[0])

    data['constraints']['cs'] = cs

def create_lp(data):
    offers = data['offers']
    customers = data['customers']
    dm = data['dm']
    cs = data['constraints']['cs']

    prob = LpProblem("chicken", LpMaximize)
    lp_vars = {}

    for customer in customers:
        lp_vars[customer] = LpVariable.dicts(("x_%s" % customer), offers, 0, 1, LpInteger)

    #print(lp_vars)

    prob += lpSum([dm[customer][offer] * lp_vars[customer][offer] for customer in customers for offer in offers]), "cost"

    for customer in customers:
        prob += lpSum([lp_vars[customer][offer] for offer in offers]) <= data['constraints'][
            'max_offer_per_customer'], ("max_offer_per_customer %s" % customer)

    prob += lpSum([lp_vars[customer][offer] for customer in customers for offer in offers]) <= data['constraints'][
        'max_total_offers'], "max_total_offers"

    max_offers = data['constraints']['max_offers']
    for key in max_offers.keys():
        prob += lpSum([lp_vars[customer][key] for customer in customers]) <= max_offers[key], ("max_offers %s" % key)

    min_offers = data['constraints']['min_offers']
    for key in min_offers.keys():
        prob += lpSum([lp_vars[customer][key] for customer in customers]) >= min_offers[key], ("min_offers %s" % key)

    for key in cs.keys():
        for enemy in cs[key]:
            for customer in customers:
                prob += lp_vars[customer][key]+lp_vars[customer][enemy] <= 1, ("%s conflicts with %s at customer %s" % (key, enemy, customer))

    return lp_vars, prob


def process_output(data, lp_vars, prob):
    offers = data['offers']
    customers = data['customers']
    dm = data['dm']

    winners = []
    for customer in customers:
        for offer in offers:
            if lp_vars[customer][offer].varValue == 1:
                winners.append("%.2f" % dm[customer][offer])

    return " + ".join(winners) + " = %.2f" % pulp.value(prob.objective)


@app.route('/solve', methods=['GET', 'POST'])
def solve():
    file_raw = ""
    if request.method == "GET":
        #output some usable default
        file = open('02-sample.json', 'r')
        file_raw = file.read()
    if request.method == "POST":
        #process POST input
        file_raw = request.json

    data = json.loads(file_raw)

    reprocess_input(data)
    lp_vars, prob = create_lp(data)

    #prob.writeLP("problem.lp")
    prob.solve()

    out_sum = process_output(data, lp_vars, prob)

    return render_template('solver.html', raw=file_raw, lp_vars=lp_vars, dm=data['dm'], offers = data['offers'], customers = data['customers'], status=pulp.LpStatus[prob.status], out_sum = out_sum)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)