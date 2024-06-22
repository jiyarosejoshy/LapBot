from flask import Flask 
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/message", methods = ["POST","GET"])
def message():
    print("kjhl")
    return {'text': 'kalkulakakulakalkula' }

if __name__ == "__main__":
    app.run(debug=True)