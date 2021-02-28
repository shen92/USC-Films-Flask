from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_landing_page():
    return app.send_static_file("index.html")

@app.route('/home', methods=['GET'])
def get_home_contents():
    response = {"message": "This is home"}
    return jsonify(response)

if __name__ == '__main__':
    app.run()