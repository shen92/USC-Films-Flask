from flask import Flask
from flask import jsonify
from flask import send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/')
def get_landing_page():
    return app.send_static_file("index.html")

@app.route('/home')
def get_home_contents():
    data = {"message": "this is info for home"}
    return jsonify(data)

@add.route('/test')
def test():
    return 'test'

if __name__ == '__main__':
    app.run()