from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__, template_folder = "./HTML", static_folder = "./Style")

@app.route('/Login', methods = ['GET', 'POST'])
def loginPage():
    if request.method == "POST":
        print("entered post")
        userData = {"email" : request.form.get("email"), "password" : request.form.get("password")}
        user = []
        user.append(userData)

        data = json.dumps(user)
        response = requests.post("http://localhost:5001/loginUser", json = data)

        print(response.json()["response"])

        if (response.json()["response"]):
            print("done")

            return redirect(url_for("home", userId = response.json()["response"]))

        print("not done")
    return render_template("login.html")

@app.route('/Register', methods = ['GET', 'POST'])
def registerPage():
    if request.method == "POST":
        userData = {"email" : request.form.get("email"), "password" : request.form.get("password")}
        user = []
        user.append(userData)

        data = json.dumps(user)
        response = requests.post('http://localhost:5001/registerUser', json = data)
        print(response.json()["response"])

        if (response.json()["response"]):
            return redirect(url_for("home", userId = response.json()["response"]))
    return render_template("creare_cont.html")

@app.route('/Home', methods = ['GET', 'POST'])
def home():
    print(request.args["userId"])

    if request.method == "POST":
        if request.form.get("alunite") == "1":
            print("alunite")
            return redirect(url_for("alunite", userId = request.args["userId"]))
        if request.form.get("stats") == "2":
            print("stats")
            return redirect(url_for("statistica", userId = request.args["userId"]))
        if request.form.get("detect") == "3":
            print("detect")

    return render_template("home.html")

@app.route('/Alunite', methods = ['GET', 'POST'])
def alunite():
    if request.method == "POST":
        print(request.form.get(request.args["userId"]))

        moleData = {"description" : request.form.get(request.args["userId"])}
        moles = []
        moles.append(moleData)

        data = json.dumps(moles)
        response = requests.post('http://localhost:5002/deleteMoles', json = data)
        if request.form.get("addMole") == "1":
            return redirect(url_for("formular", userId = request.args["userId"]))


    userData = {"id" : request.args["userId"]}
    user = []
    user.append(userData)

    data = json.dumps(user)
    response = requests.post('http://localhost:5002/loadMoles', json = data)

    return render_template("tabel.html", moles = response.json()["Response"])

@app.route('/Formular', methods = ['GET', 'POST'])
def formular():
    if request.method == "POST":
        moleData = {
                    "User" : request.args["userId"],
                    "Date" : request.form.get("date"),
                    "isCarcinogenic" : int(request.form.get("isCarcinogenic")),
                    "BodyLocation" : request.form.get("bodyLocation"),
                    "Size" : request.form.get("size"),
                    "Shape" : request.form.get("shape"),
                    "isSymmetrical" : int(request.form.get("isSymmetrical")),
                    "Color" : request.form.get("color"),
                    "Description" : request.form.get("observation"),
                    "Grade" : int(request.form.get("grade")),
                    }
        print(moleData)

        moles = []
        moles.append(moleData)
        data = json.dumps(moles)

        response = requests.post('http://localhost:5002/registerMoles', json = data)
        if response.json()["response"] == 1:
            return redirect(url_for("alunite", userId = request.args["userId"]))

    return render_template("formular.html")

@app.route('/Statistica', methods = ['GET', 'POST'])
def statistica():
    userData = {"id" : request.args["userId"]}
    user = []
    user.append(userData)

    data = json.dumps(user)
    response = requests.post('http://localhost:5002/loadMoles', json = data)

    moleData = json.dumps(response.json()["Response"])
    stats = requests.post('http://localhost:5003/calculateStats', json = moleData)

    return render_template("statistica.html", stats = stats.json()["response"])
# driver function
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000)