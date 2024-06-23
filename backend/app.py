from flask import Flask ,request , jsonify
from flask_cors import CORS
app = Flask(__name__)
from model import query
CORS(app)
@app.route("/message", methods = ["POST","GET"])
def message():
    print("kjhl")
    input_text = request.json.get("text")
    response =  query(input_text)
    print(type(response))
    return jsonify({'text': response })

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")