import json
from flask import Flask, abort, jsonify, request
from flask_restful import Resource, Api
import certifi

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8'] # this is a google public dns server, use whatever dns server you like here # as a test, dns.resolver.query(‘www.google.com 4’) should return an answer, not an exception

from pymongo import MongoClient
dataBaseHostUrl = "mongodb+srv://ioanamorariu01:vB3SKOVymREGxdQO@cluster0.0gbyxid.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
dataBaseClient = MongoClient(dataBaseHostUrl, tlsCaFile=certifi.where())

app = Flask(__name__)
api = Api(app)

@app.route('/registerMoles', methods=['GET', 'POST'])
def registerMoles():
    if request.method == "POST":
        data = json.loads(request.get_json())

        for value in data:
            print(value)
            moleData = {
                    "User" : value["User"],
                    "Date" : value["Date"],
                    "IsCarcinogenic" : value["isCarcinogenic"],
                    "BodyLocation" : value["BodyLocation"],
                    "Size" : value["Size"],
                    "Shape" : value["Shape"],
                    "IsSymmetrical" : value["isSymmetrical"],
                    "Color" : value["Color"],
                    "Description" : value["Description"],
                    "Grade" : value["Grade"],
                    }
            dataBaseClient.Mole.Moles.insert_one(moleData)

    responseBody = {"response" : 1}
    response = app.response_class(
        response=json.dumps(responseBody),
        status=200,
        mimetype='application/json'
    )

    return response
@app.route('/loadMoles', methods=['GET', 'POST'])
def loadMoles():
    if request.method == "POST":
        data = json.loads(request.get_json())

        for value in data:
            moles = dataBaseClient.Mole.Moles.find({"User" : value["id"]})

            responseAnswer = {"Response" : []}
            for mole in moles:
                moleData = {
                            "User" : mole["User"],
                            "Date" : mole["Date"],
                            "IsCarcinogenic" : mole["IsCarcinogenic"],
                            "BodyLocation" : mole["BodyLocation"],
                            "Size" : mole["Size"],
                            "Shape" : mole["Shape"],
                            "IsSymmetrical" : mole["IsSymmetrical"],
                            "Color" : mole["Color"],
                            "Description" : mole["Description"],
                            "Grade" : mole["Grade"],
                            }

                responseAnswer["Response"].append(moleData)

        response = app.response_class(
                            response=json.dumps(responseAnswer),
                            status=200,
                            mimetype='application/json'
                            )

    return response

@app.route('/deleteMoles', methods=['GET', 'POST'])
def deleteMoles():
    if request.method == "POST":
        data = json.loads(request.get_json())

        for value in data:
            dataBaseClient.Mole.Moles.delete_one({"Description" : value["description"]})

        responseBody = {"response" : 1}
        response = app.response_class(
                            response=json.dumps(responseBody),
                            status=200,
                            mimetype='application/json'
                            )

    return response

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)