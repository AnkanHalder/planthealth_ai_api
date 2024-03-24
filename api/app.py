from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return {
        "message": "Welcome to API for Planthealth AI"
    }
