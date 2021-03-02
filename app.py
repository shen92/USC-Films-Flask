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
@app.route('/static/index.html', methods=['GET'])
def get_landing_page():
    return app.send_static_file("index.html")

@app.route('/home/movies', methods=['GET'])
def get_home_movies():
    url = Template('$base_url/trending/movie/week?api_key=$api_key').substitute(base_url=BASE_URL, api_key=API_KEY)
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"]
        results = results[0:5]
        response = []
        for result in results:
            movie = {
                "title": result["title"], 
                "backdrop_path": result["backdrop_path"],
                "release_date": result["release_date"]
                }
            response.append(movie)
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response), api_response.status_code

@app.route('/home/tvshows', methods=['GET'])
def get_home_tv_shows():
    url = Template('$base_url/tv/airing_today?api_key=$api_key').substitute(base_url=BASE_URL, api_key=API_KEY)
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"]
        results = results[0:5]
        response = []
        for result in results:
            tvshow = {
                "name": result["name"], 
                "backdrop_path": result["backdrop_path"],
                "first_air_date": result["first_air_date"]
                }
            response.append(tvshow)
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response), api_response.status_code

@app.route('/search/movie', methods=['GET'])
def get_search_movies():
    params = request.args
    url = Template('$base_url/search/movie?api_key=$api_key&query=$keyword&language=en-US&page=1&include_adult=false').substitute(base_url=BASE_URL, api_key=API_KEY,keyword=params["keyword"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"]
        results = results[0:10]
        response = []
        for result in results:
            movie = {
                "id": result["id"], 
                "title": result["title"],
                "overview": result["overview"],
                "poster_path": result["poster_path"],
                "release_date": result["release_date"],
                "vote_average": result["vote_average"], 
                "vote_count": result["vote_count"], 
                "genre_ids": result["genre_ids"],
                "media_type": "movie"
                }
            response.append(movie)
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response), api_response.status_code

@app.route('/search/tv', methods=['GET'])
def get_search_tv_shows():
    params = request.args
    url = Template('$base_url/search/tv?api_key=$api_key&query=$keyword&language=en-US&page=1&include_adult=false').substitute(base_url=BASE_URL, api_key=API_KEY,keyword=params["keyword"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"]
        results = results[0:10]
        response = []
        for result in results:
            tvshow = {
                "id": result["id"],
                "name": result["name"],
                "overview": result["overview"],
                "poster_path": result["poster_path"],
                "first_air_date": result["first_air_date"],
                "vote_average": result["vote_average"],
                "vote_count": result["vote_count"],
                "genre_ids": result["genre_ids"],
                "media_type": "tv"
                }
            response.append(tvshow)
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response), api_response.status_code

@app.route('/search/multi', methods=['GET'])
def get_search_multi():
    params = request.args
    url = Template('$base_url/search/multi?api_key=$api_key&query=$keyword&language=en-US&page=1&include_adult=false').substitute(base_url=BASE_URL, api_key=API_KEY,keyword=params["keyword"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"]
        response = []
        for result in results:
            if(result["media_type"] == "movie"):
                data = {
                    "id": result["id"], 
                    "title": result["title"],
                    "overview": result["overview"],
                    "poster_path": result["poster_path"],
                    "release_date": result["release_date"],
                    "vote_average": result["vote_average"], 
                    "vote_count": result["vote_count"], 
                    "genre_ids": result["genre_ids"],
                    "media_type": "movie"
                    }
                response.append(data)
            elif(result["media_type"] == "tv"):
                data = {
                    "id": result["id"],
                    "name": result["name"],
                    "overview": result["overview"],
                    "poster_path": result["poster_path"],
                    "first_air_date": result["first_air_date"],
                    "vote_average": result["vote_average"],
                    "vote_count": result["vote_count"],
                    "genre_ids": result["genre_ids"],
                    "media_type": "tv"
                }
                response.append(data)
        response = response[0:10]
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response), api_response.status_code

if __name__ == '__main__':
    app.run()