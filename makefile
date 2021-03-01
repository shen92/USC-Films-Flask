init:
	rm -rf venv/
	python3 -m venv venv

activate:
	. venv/bin/activate

install:
	pip install Flask
	pip install Flask-Cors
	pip install requests

web:
	live-server --port=3000

flask:
	export FLASK_APP=app.py
	flask run

deploy:
	rm -rf requirements.txt
	pip freeze > requirements.txt
	git add .
	git commit -m "deploy latest build"
	git push