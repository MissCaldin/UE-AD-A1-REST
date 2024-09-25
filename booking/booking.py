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
def get_json_user(userid):
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
def post_json_booking(userid):
   req = request.get_json()

   for booking in bookings:
      if str(booking["userid"]) == str(userid):
         date_req = str(req['date'])
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

def write(something):
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        json.dump(something, f)




if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
