import json
from flask import Flask, abort, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route('/calculateStats', methods=['GET', 'POST'])
def calculateStats():
    data = json.loads(request.get_json())
    totalNumberOfMoles = len(data)
    carcinogenicMoles = 0
    smallAndSimetricMoles = 0
    brownColorMoles = 0
    bigAndRedColoredMoles = 0
    under5GradeMoles = 0

    for value in data:
        print(value)
        if value["IsCarcinogenic"] == 1:
            carcinogenicMoles += 1
        if value["Size"] == "mică" and value["IsSymmetrical"] == 1:
            smallAndSimetricMoles += 1
        if value["Color"] == "brună":
            brownColorMoles += 1
        if value["Size"] == "mare" and value["Color"] == "roșiatică":
            bigAndRedColoredMoles += 1
        if value["Grade"] < 5:
            under5GradeMoles += 1

    carcinogenicMolesPercent = round((carcinogenicMoles / totalNumberOfMoles) * 100, 2)
    brownColorMolesPercent = round((brownColorMoles / totalNumberOfMoles) * 100, 2)

    responseBody = {"response" :
                        {"TotalNumberOfMoles" : totalNumberOfMoles,
                        "CarcinogenicMolesPercent" : carcinogenicMolesPercent,
                        "BrownColorMolesPercent" : brownColorMolesPercent,
                        "SmallAndSimetricMoles" : smallAndSimetricMoles,
                        "BigAndRedColoredMoles" : bigAndRedColoredMoles,
                        "Under5GradeMoles" : under5GradeMoles}}

    response = app.response_class(
        response=json.dumps(responseBody),
        status=200,
        mimetype='application/json'
    )

    return response
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)