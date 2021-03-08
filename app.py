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
NUM_RESULTS = 10
NUM_CASTS = 8
NUM_COMMENTS = 5

@app.route('/', methods=['GET'])
def get_landing_page():
    return app.send_static_file("index.html")

#2.1.1 TMDB Trending Endpoint
@app.route('/home/movie', methods=['GET'])
def get_home_movies():
    url = Template('$base_url/trending/movie/week?api_key=$api_key').substitute(base_url=BASE_URL, api_key=API_KEY)
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"] if "results" in results else []
        results = results[0:5]
        response = []
        for result in results:
            movie = {
                "title": result["title"] if "title" in result else None, 
                "backdrop_path": result["backdrop_path"] if "backdrop_path" in result else None,
                "release_date": result["release_date"] if "release_date" in result else None,   
                "media_type": "movie" #Additional field
            }
            response.append(movie)
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.1.2 TMDB TV Airing Today Endpoint
@app.route('/home/tv', methods=['GET'])
def get_home_tv_shows():
    url = Template('$base_url/tv/airing_today?api_key=$api_key').substitute(base_url=BASE_URL, api_key=API_KEY)
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"] if "results" in results else []
        results = results[0:5]
        response = []
        for result in results:
            tvshow = {
                "name": result["name"] if "name" in result else None, 
                "backdrop_path": result["backdrop_path"] if "backdrop_path" in result else None,
                "first_air_date": result["first_air_date"] if "first_air_date" in result else None,
                "media_type": "tv"  #Additional field
            }
            response.append(tvshow)
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.3.1 Search Movie Endpoint
@app.route('/search/movie', methods=['GET'])
def get_search_movies():
    params = request.args
    url = Template('$base_url/search/movie?api_key=$api_key&query=$keyword&language=en-US&page=1&include_adult=false').substitute(base_url=BASE_URL, api_key=API_KEY,keyword=params["keyword"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"] if "results" in results else []
        results = results[0:NUM_RESULTS] 
        response = []
        for result in results:
            movie = {
                "id": result["id"] if "id" in result else None, 
                "title": result["title"] if "title" in result else None,
                "overview": result["overview"] if "overview" in result else None,
                "poster_path": result["poster_path"] if "poster_path" in result else None,
                "release_date": result["release_date"] if "release_date" in result else None,
                "vote_average": result["vote_average"] if "vote_average" in result else None, 
                "vote_count": result["vote_count"] if "vote_count" in result else None, 
                "genre_ids": result["genre_ids"] if "genre_ids" in result else None,
                "media_type": "movie" #Additional field
                }
            response.append(movie)
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.3.2 Search TV Endpoint
@app.route('/search/tv', methods=['GET'])
def get_search_tv_shows():
    params = request.args
    url = Template('$base_url/search/tv?api_key=$api_key&query=$keyword&language=en-US&page=1&include_adult=false').substitute(base_url=BASE_URL, api_key=API_KEY,keyword=params["keyword"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"] if "results" in results else []
        results = results[0:NUM_RESULTS] 
        response = []
        for result in results:
            tvshow = {
                "id": result["id"] if "id" in result else None,
                "name": result["name"] if "name" in result else None,
                "overview": result["overview"] if "overview" in result else None,
                "poster_path": result["poster_path"] if "poster_path" in result else None,
                "first_air_date": result["first_air_date"] if "first_air_date" in result else None,
                "vote_average": result["vote_average"] if "vote_average" in result else None,
                "vote_count": result["vote_count"] if "vote_count" in result else None,
                "genre_ids": result["genre_ids"] if "genre_ids" in result else None,
                "media_type": "tv"  #Additional field
                }
            response.append(tvshow)
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.3.3 Multi-Search Endpoint
@app.route('/search/multi', methods=['GET'])
def get_search_multi():
    params = request.args
    url = Template('$base_url/search/multi?api_key=$api_key&query=$keyword&language=en-US&page=1&include_adult=false').substitute(base_url=BASE_URL, api_key=API_KEY,keyword=params["keyword"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"] if "results" in results else []
        response = []
        for result in results:
            if("media_type" in result and result["media_type"] == "movie"):
                data = {
                    "id": result["id"] if "id" in result else None, 
                    "title": result["title"] if "title" in result else None,
                    "overview": result["overview"] if "overview" in result else None,
                    "poster_path": result["poster_path"] if "poster_path" in result else None,
                    "release_date": result["release_date"] if "release_date" in result else None,
                    "vote_average": result["vote_average"] if "vote_average" in result else None, 
                    "vote_count": result["vote_count"] if "vote_count" in result else None, 
                    "genre_ids": result["genre_ids"] if "genre_ids" in result else None,
                    "media_type": "movie" #Additional field
                    }
                response.append(data)
            elif("media_type" in result and result["media_type"] == "tv"):
                data = {
                    "id": result["id"] if "id" in result else None,
                    "name": result["name"] if "name" in result else None,
                    "overview": result["overview"] if "overview" in result else None,
                    "poster_path": result["poster_path"] if "poster_path" in result else None,
                    "first_air_date": result["first_air_date"] if "first_air_date" in result else None,
                    "vote_average": result["vote_average"] if "vote_average" in result else None,
                    "vote_count": result["vote_count"] if "vote_count" in result else None,
                    "genre_ids": result["genre_ids"] if "genre_ids" in result else None,
                    "media_type": "tv" #Additional field
                }
                response.append(data)
        response = response[0:NUM_RESULTS]
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.5.1 TMDB Movie Genres Endpoint
@app.route('/genres/movie', methods=['GET'])
def get_movie_genres(): 
    url = Template('$base_url/genre/movie/list?api_key=$api_key&language=en-US').substitute(base_url=BASE_URL, api_key=API_KEY)
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        response = results["genres"] if "genres" in results else []
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.5.2 TMDB TV Genres Endpoint
@app.route('/genres/tv', methods=['GET'])
def get_tv_show_genres():
    url = Template('$base_url/genre/tv/list?api_key=$api_key&language=en-US').substitute(base_url=BASE_URL, api_key=API_KEY)
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        response = results["genres"] if "genres" in results else []
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.4.1 Get Movie Details Endpoint
@app.route('/details/movie', methods=['GET'])
def get_movie_details():
    params = request.args
    url = Template('$base_url/movie/$id?api_key=$api_key&language=en-US').substitute(base_url=BASE_URL, api_key=API_KEY,id=params["id"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        result = api_response.json()
        data = {
            "id": result["id"] if "id" in result else None,
            "title": result["title"] if "title" in result else None,
            "runtime": result["runtime"] if "runtime" in result else None,
            "release_date": result["release_date"] if "release_date" in result else None,
            "spoken_languages": result["spoken_languages"] if "spoken_languages" in result else None,
            "vote_average": result["vote_average"] if "vote_average" in result else None,
            "vote_count": result["vote_count"] if "vote_count" in result else None,
            "poster_path": result["poster_path"] if "poster_path" in result else None,
            "backdrop_path": result["backdrop_path"] if "backdrop_path" in result else None,
            "genres": result["genres"] if "genres" in result else None,
            "overview": result["overview"] if "overview" in result else None, #Additional field
            "media_type": "movie"   #Additional field
        }
        return jsonify({"data": data})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.4.4 Get TV Show Details Endpoint
@app.route('/details/tv', methods=['GET'])
def get_tv_details():
    params = request.args
    url = Template('$base_url/tv/$id?api_key=$api_key&language=en-US').substitute(base_url=BASE_URL, api_key=API_KEY,id=params["id"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        result = api_response.json()
        data = {
            "backdrop_path": result["backdrop_path"] if "backdrop_path" in result else None,
            "episode_run_time": result["episode_run_time"] if "episode_run_time" in result else None,
            "first_air_date": result["first_air_date"] if "first_air_date" in result else None,
            "genres": result["genres"] if "genres" in result else None,
            "id": result["id"] if "id" in result else None,
            "name": result["name"] if "name" in result else None,
            "number_of_seasons": result["number_of_seasons"] if "number_of_seasons" in result else None,
            "overview": result["overview"] if "overview" in result else None,
            "poster_path": result["poster_path"] if "poster_path" in result else None,
            "spoken languages": result["spoken languages"] if "spoken languages" in result else None,
            "vote_average": result["vote_average"] if "vote_average" in result else None,
            "vote_count": result["vote_count"] if "vote_count" in result else None, #Additional field
            "overview": result["overview"] if "overview" in result else None, #Additional field
            "media_type": "tv"
        }
        return jsonify({"data": data})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.4.2 Get Movie Credits Endpoint
@app.route('/cast/movie', methods=['GET'])
def get_movie_cast():
    params = request.args
    url = Template('$base_url/movie/$id/credits?api_key=$api_key&language=en-US').substitute(base_url=BASE_URL, api_key=API_KEY,id=params["id"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["cast"] if "cast" in results else []
        results = results[0:NUM_CASTS]
        response = []
        for result in results:
            data = {
                "name": result["name"] if "name" in result else None,
                "profile_path": result["profile_path"] if "profile_path" in result else None,
                "character": result["character"] if "character" in result else None,
            }
            response.append(data)
        return jsonify({"data": results})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.4.5 Get TV Show Credits Endpoint
@app.route('/cast/tv', methods=['GET'])
def get_tv_cast():
    params = request.args
    url = Template('$base_url/tv/$id/credits?api_key=$api_key&language=en-US').substitute(base_url=BASE_URL, api_key=API_KEY,id=params["id"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["cast"] if "cast" in results else []
        results = results[0:NUM_CASTS]
        response = []
        for result in results:
            data = {
                "name": result["name"] if "name" in result else None,
                "profile_path": result["profile_path"] if "profile_path" in result else None,
                "character": result["character"] if "character" in result else None,
            }
            response.append(data)
        return jsonify({"data": results})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.4.3 Get Movie Reviews Endpoint
@app.route('/reviews/movie', methods=['GET'])
def get_movie_reviews():
    params = request.args
    url = Template('$base_url/movie/$id/reviews?api_key=$api_key&language=en-US').substitute(base_url=BASE_URL, api_key=API_KEY,id=params["id"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"] if "results" in results else []
        results = results[0:NUM_COMMENTS]
        response = []
        for result in results:
            author_details = result["author_details"] if "author_details" in result else None
            data = {
                "username": author_details["username"] if author_details is not None and "username" in author_details else None,
                "content": result["content"] if "content" in result else None,
                "rating": author_details["rating"] if author_details is not None and "rating" in author_details else None,
                "created_at": result["created_at"] if "created_at" in result else None,
            }
            response.append(data)
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

#2.4.6 Get TV Show Reviews Endpoint
@app.route('/reviews/tv', methods=['GET'])
def get_tv_reviews():
    params = request.args
    url = Template('$base_url/tv/$id/reviews?api_key=$api_key&language=en-US').substitute(base_url=BASE_URL, api_key=API_KEY,id=params["id"])
    api_response = requests.get(url)
    if api_response.status_code == 200:
        #Extract response
        results = api_response.json()
        results = results["results"] if "results" in results else []
        results = results[0:NUM_COMMENTS]
        response = []
        for result in results:
            author_details = result["author_details"] if "author_details" in result else None
            data = {
                "username": author_details["username"] if author_details is not None and "username" in author_details else None,
                "content": result["content"] if "content" in result else None,
                "rating": author_details["rating"] if author_details is not None and "rating" in author_details else None,
                "created_at": result["created_at"] if "created_at" in result else None,
            }
            response.append(data)
        return jsonify({"data": response})
    else:
        response = {"message": "Unknown error occurred."}
        return jsonify(response)

if __name__ == '__main__':
    app.run()