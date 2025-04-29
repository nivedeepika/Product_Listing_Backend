from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import os
from urllib.parse import quote_plus

password = "Deepika@2003"
encoded_password = quote_plus(password)



app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# MongoDB setup
client = MongoClient("mongodb+srv://deepikanivedeepika:Deepika%402003@cluster0.7jhmlxy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['userAuth']
users = db['users']

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    mobile = data["mobile"]
    password = data["password"]

    if users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users.insert_one({
        "name": name,
        "email": email,
        "mobile": mobile,
        "password": hashed_pw
    })

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = users.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "name": user["name"]}), 200

if __name__ == "__main__":
    app.run(debug=True)
