from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import requests

from string import Template
import json

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = 'ffacc501334b9c13b0136b785a4a2d81'

@app.route('/', methods=['GET'])
def get_landing_page():
    return app.send_static_file("index.html")

@app.route('/home/movies', methods=['GET'])
def get_home_movies():
    url = Template('$base_url/trending/movie/week?api_key=$api_key').substitute(base_url=BASE_URL, api_key=API_KEY)
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Process data from TMDB
        result = api_response.json()
        result = result["results"]
        result = result[0:5]
        return jsonify({'data': result}), api_response.status_code
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response), api_response.status_code

@app.route('/home/tvshows', methods=['GET'])
def get_home_tv_shows():
    url = Template('$base_url/tv/airing_today?api_key=$api_key').substitute(base_url=BASE_URL, api_key=API_KEY)
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Process data from TMDB
        result = api_response.json()
        result = result["results"]
        result = result[0:5]
        return jsonify({'data': result}), api_response.status_code
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response), api_response.status_code

@app.route('/search', methods=['GET'])
def get_query_results():
    params = request.args
    url = Template('$base_url/search/$category?api_key=$api_key&query=$keyword&language=en-US&page=1&include_adult=false').substitute(base_url=BASE_URL, api_key=API_KEY,category=params["category"],keyword=params["keyword"])
    api_response = requests.get(url)
    result = api_response.json()
    result = result["results"]
    result = result[0:10]
    return jsonify({'data': result}), api_response.status_code

if __name__ == '__main__':
    app.run()