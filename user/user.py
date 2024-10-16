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
   url=f"http://127.0.0.1:3201/showmovies/{date}"
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
   return make_response(jsonify({pretty_date(date): response}), 200)

@app.route("/movieschedule/<movieid>", methods=['GET'])
def movieschedule(movieid):
   url=f"http://127.0.0.1:3200/movies/{movieid}"
   response1=requests.get(url)
   if response1.status_code == 400:
      return response1
   title=response1.json()["title"]

   url=f"http://127.0.0.1:3201/movieschedule/{movieid}"
   response2 = requests.get(url)
   if response2.status_code == 400:
      return response2
   
   response=[]
   rep_json = response2.json()

   for date in rep_json[movieid]:
      response.append(pretty_date(date))
   
   return make_response(jsonify({title: response}), 200)

@app.route("/<string:id>", methods=["GET"])
def home_user(id):
   user = next((user for user in users if user['id'] == id), None)
   if user==None:
      return jsonify({"error": "User not found"}), 404
   return make_response(jsonify(user['name']))

# Get bookings for a specific user
@app.route("/<string:userid>/bookings", methods=["GET"])
def get_bookings_for_user(userid):
    # Appel au service Booking pour obtenir les réservations de l'utilisateur
    try:
        response = requests.get(f"http://127.0.0.1:3201/booking/{userid}")
        if response.status_code == 200:
            bookings = response.json()
            return jsonify(bookings), 200
        else:
            return jsonify({"error": "User not found or no bookings available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get information about a movie reserved by the user
@app.route("/<string:userid>/<string:movieid>", methods=["GET"])
def get_movie(userid, movieid):
    try:
        # Appel au service Booking pour vérifier si l'utilisateur a réservé ce film
        booking_response = requests.get(f"http://127.0.0.1:3201/booking/{userid}")
        
        # Vérifier si la réponse du service Booking est valide
        if booking_response.status_code != 200:
            return jsonify({"error": "User not found or no bookings available"}), 404

        # Récupérer la réponse JSON
        bs = booking_response.json()

        # La réponse est une liste, il faut donc accéder au premier élément
        if not isinstance(bs, list) or len(bs) == 0:
            return jsonify({"error": "No bookings found for this user"}), 404
        
        # On suppose qu'il n'y a qu'un seul objet dans la liste (un seul utilisateur)
        user_bookings = bs[0]
        # Vérifier si la clé 'dates' est présente dans la réponse
        if 'dates' not in user_bookings:
            return jsonify({"error": "No bookings found for this user"}), 404
        
        # Extraire les réservations (dates et films associés)
        bookings = user_bookings['dates']

        # Vérifier si le film fait partie des réservations pour n'importe quelle date
        movie_reserved = any(movieid in date["movies"] for date in bookings)
        
        if not movie_reserved:
            return jsonify({"error": "Movie not reserved by this user"}), 403
        

        # Si le film est réservé, récupérer les détails du film depuis le service Movie
        movie_response = requests.get(f"http://127.0.0.1:3200/movies/{movieid}")
        
        if movie_response.status_code == 200:
            movie_info = movie_response.json()
            return jsonify(movie_info), 200
        else:
            return jsonify({"error": "Movie not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def pretty_date(date):
   return date[6:]+'/'+date[4:6]+'/'+date[:4]

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
