import json
from flask import Flask, abort, jsonify, request
from flask_restful import Resource, Api
import certifi

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8'] # this is a google public dns server, use whatever dns server you like here # as a test, dns.resolver.query(‘www.google.com 4’) should return an answer, not an exception

from pymongo import MongoClient
dataBaseHostUrl = "mongodb+srv://ioanamorariu01:luuqaL8kdWAxbyL1@cluster0.a128kpq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
dataBaseClient = MongoClient(dataBaseHostUrl, tlsCaFile=certifi.where())

app = Flask(__name__)
api = Api(app)

@app.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
    if request.method == "POST":
        print("Received Post")
    if request.method == "GET":
        print("Received Get")
    if not request.json:
        print("No json!")

    data = json.loads(request.get_json())

    print(data)

    for value in data:
        print(value)
        result = dataBaseClient.User.Users.insert_one({
            "Email": value["email"],
            "Password": value["password"]
            })

    if not result:
        print("Issue inserting into database!")

    responseAnswer = {"response" : str(result.inserted_id)}
    response = app.response_class(
        response=json.dumps(responseAnswer),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
    if request.method == "POST":
        data = json.loads(request.get_json())

        print(data)
        for value in data:
            print(value)
            user = dataBaseClient.User.Users.find_one({"Email" : value["email"], "Password" : value["password"]})
            print(user)
            if user:
                print("found")
                responseAnswer = {"response" : str(user["_id"])}
                response = app.response_class(
                    response=json.dumps(responseAnswer),
                    status=200,
                    mimetype='application/json'
                )
                return response


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)