pip freeze > requirements.txt
COMMIT_ID=$(git rev-parse --verify HEAD)
git add .
git commit -m "deploy build ${COMMIT_ID}"
git push
