from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/movies", methods=['GET'])
def movies():
   url="http://127.0.0.1:3200/json"
   response = requests.get(url)
   return make_response(jsonify(response.json()), 200)

@app.route("/showmovies/<date>", methods=['GET'])
def showmovies(date):
   url=f"http://127.0.0.1:3202/showmovies/{date}"
   ids_date = requests.get(url)
   if ids_date.status_code == 400:
      return make_response(jsonify({"error":"No movie this day"}),400)
   response=[]
   ids = ids_date.json()
   for id_movie in ids[date]:
      print(id_movie)
      url2=f"http://127.0.0.1:3200/movies/{id_movie}"
      title = requests.get(url2).json()["title"]
      response.append(title)
   date_format = date[6:]+'/'+date[4:6]+'/'+date[:4]
   return make_response(jsonify({date_format: response}), 200)

@app.route("/movieschedule/<movieid>", methods=['GET'])
def movieschedule(movieid):
   url=f"http://127.0.0.1:3200/movies/{movieid}"
   response1=requests.get(url)
   if response1.status_code == 400:
      return response1
   title=response1.json()["title"]

   url=f"http://127.0.0.1:3202/movieschedule/{movieid}"
   response2 = requests.get(url)
   if response2.status_code == 400:
      return response2
   
   response=[]
   rep_json = response2.json()

   def pretty_date(date):
      return date[6:]+'/'+date[4:6]+'/'+date[:4]

   for date in rep_json[movieid]:
      response.append(pretty_date(date))
   
   return make_response(jsonify({title: response}), 200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
