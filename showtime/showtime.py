from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/showtimes", methods=['GET'])
def showtimes():
   res = make_response(jsonify(schedule), 200)
   return res

@app.route("/showmovies/<date>", methods=['GET'])
def showmovies(date):
   for day in schedule:
      if str(day["date"]) == str(date):
         return make_response(jsonify({date:day["movies"]}),200)
         
   return make_response(jsonify({"error":"No movie this day"}),400)

@app.route("/movieschedule/<movieid>", methods=['GET'])
def movieschedule(movieid):
   response=[]
   for day in schedule:
      for id_movie in day["movies"]:
         if id_movie==movieid:
            response.append(day["date"])
            break
   if response == []:
      return make_response(jsonify({"error":"This film is not scheduled"}),400)

   return make_response(jsonify({movieid:response}), 200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
