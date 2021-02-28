from flask import Flask
from flask import jsonify
from flask_cors import CORS
import requests

from string import Template

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = 'ffacc501334b9c13b0136b785a4a2d81'

@app.route('/', methods=['GET'])
def get_landing_page():
    return app.send_static_file("index.html")

@app.route('/home/movies', methods=['GET'])
def get_home_contents():
    url = Template('$base_url/trending/movie/week?api_key=$api_key').substitute(base_url=BASE_URL, api_key=API_KEY)
    api_response = requests.get(url)
    if api_response.status_code == 200:
        response = api_response.json()
        return response
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response), api_response.status_code

if __name__ == '__main__':
    app.run()