from flask import Flask
from flask import jsonify
from flask import send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_landing_page():
    return app.send_static_file("index.html")

@app.route('/home', methods=['GET'])
def get_home_contents():
    response = {"message": "this is home"}
    return jsonify(response)

if __name__ == '__main__':
    app.run()