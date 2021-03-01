rm -rf requirements.txt
pip freeze > requirements.txt
current_git_branch_latest_short_id=`git rev-parse --short HEAD`
git add .
git commit -m "deploy build from ${current_git_branch_latest_short_id}"
git push
