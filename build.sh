#!/bin/zsh
python scrape.py && python process.py && python model.py
git add . && git commit -m "updated model"
# remote origin 
git push origin master
# deploy on heroku
git push heroku master 
