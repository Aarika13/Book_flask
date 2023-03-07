from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home(name):
    return "Hello"
if __name__ == '__main__':
    app.run()