from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hi_world(): 
    return "Hola Mundo"

@app.route('/api/users/')
def hi(): 
    print(request.headers.get('token', None))
    return "Hola user"


@app.route('/ping/', methods=['GET'])
def hi2(): 
    print(request.headers.get('token', None))
    return {"p": "pong"}