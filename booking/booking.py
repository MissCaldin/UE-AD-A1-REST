from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]


# Path "/" for the home page
@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


#Path "/bookings" Print the JSON Database (GET)
@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res

#Path "/booking/{userid}" 
#Print the JSON bookinks of the userid (GET)
#Add a booking for a user (POST)
@app.route("/booking/<userid>", methods=['GET'])
def get_bookung_for_user(userid):
   user_bookings = []
   for booking in bookings:
     if booking["userid"] == userid:
         user_bookings.append(booking)
   if not user_bookings:
     res = make_response(jsonify({"error": "Unknown user"}), 400)
   else:
     # Retourner toutes les réservations trouvées
     res = make_response(jsonify(user_bookings), 200)
   return res

@app.route("/booking/<userid>", methods=['POST'])
def add_booking_byuser(userid):
   req = request.get_json()

   date_req = str(req['date'])
   #Récupérer les films projettés à cette date
   url = f"http://127.0.0.1:3202/showmovies/{date_req}"
   result = requests.get(url)
   if result.status_code == 200:
      movies = result.json()
      #Vérifier que le film souhaité est bien dans les films projettés à cette date
      if str(req['movieid']) in movies:
         #Vérifier que la reservation n'a pas déjà été faite
         for booking in bookings:
            if str(booking["userid"]) == str(userid):
               for date in booking["dates"]:
                  if str(date['date'])==date_req:
                     return make_response(jsonify({"error":"A booking already exists"}),409)
               date = {
                  "date": date_req,
                  "movies": str(req['movieid'])
               }
               booking["dates"].append(date)
               write(bookings)
               res = make_response(jsonify({"message":"movie added"}),200)
               return res
      else:
         return make_response((jsonify({"error": "Créneau inexistant"}), 409))
   
   else:
      return make_response((jsonify({"error": "Erreur lors de la récupération des films"}), 409))

@app.route("/showtimes", methods=['GET'])
def showtime():
   url=f"http://127.0.0.1:3202/showtimes"
   response=requests.get(url)
   return make_response(jsonify(response.json()), response.status_code)

@app.route("/showmovies/<date>", methods=['GET'])
def showmovies(date):
   url=f"http://127.0.0.1:3202/showmovies/{date}"
   response=requests.get(url)
   return make_response(jsonify(response.json()), response.status_code)

@app.route("/movieschedule/<movieid>", methods=['GET'])
def movieschedule(movieid):
   url=f"http://127.0.0.1:3202/movieschedule/{movieid}"
   response=requests.get(url)
   return make_response(jsonify(response.json()), response.status_code)
   

def write(something):
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
        json.dump(something, f, indent=4)




if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
