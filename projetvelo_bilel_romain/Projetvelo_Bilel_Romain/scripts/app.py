import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import requests
import json
import math

# Configuration
JCDECAUX_API_KEY = "5d1f897a78c153cd920389d50f769e7f61c5e08f" # ma clé API JCDecaux
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijc2YTJkMjcyNTQ4OTRhZDU4ZjY5NTM4ZDgwNWI1NGQzIiwiaCI6Im11cm11cjY0In0=" # clé pour les trajets (openrouteservice)

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'ODG-main')) # setup de l'app flask

# Configuration BDD
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.secret_key = 'super_secret_key_bilel_romain' # Nécessaire pour les sessions

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # La vue à afficher si on n'est pas connecté

# Base de données
db = SQLAlchemy()
db.init_app(app)

# Modèle User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    preferedcity = db.Column(db.String(250), nullable=True)
    lastitinerary = db.Column(db.String(250), nullable=True)

# Création des tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def get_distance_km(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon pour le calcul
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/')
@login_required
def index():
    user_city = None
    if current_user.preferedcity:
        user_city = current_user.preferedcity
    
    return render_template('app_template.html', user=current_user, user_city=user_city)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    error = None
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        if action == 'register':
            # Création de compte
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return render_template('login.html', error="Cet utilisateur existe déjà")
            
            new_user = User(username=username, password=password) # Hash password en prod !
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
            
        elif action == 'login':
            # Connexion
            user = User.query.filter_by(username=username).first()
            if user and user.password == password: # Check hash en prod !
                login_user(user)
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error="Mauvais identifiant ou mot de passe")

    return render_template('login.html')

@app.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/updateProfile', methods=['POST'])
@login_required
def update_profile():
    data = request.json
    city = data.get('city')
    itinerary_info = data.get('itinerary')
    
    if city:
        current_user.preferedcity = city
    if itinerary_info:
        current_user.lastitinerary = json.dumps(itinerary_info) # Store as JSON string
        
    db.session.commit()
    return jsonify({'status': 'ok'})

def get_ors_route(lat1, lng1, lat2, lng2, profile):
    # fonction pour appeler l'API de trajet
    # profile c'est si on est a pied ou en vélo
    if not ORS_API_KEY:
        print("Erreur: Pas de clé API ORS")
        return None

    headers = {
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }
    body = {
        "coordinates": [[lng1, lat1], [lng2, lat2]]
    }
    
    url = f'https://api.openrouteservice.org/v2/directions/{profile}/geojson'
    
    try:
        # on tente l'appel
        r = requests.post(url, json=body, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"Galere ORS {r.status_code}: {r.text}")
            return None
        return r.json()
    except Exception as e:
        print(f"Exception ORS: {e}")
        return None

@app.route('/api/getTrajectory')
def get_trajectory():
    #  coords en float sinon ça marche pas
    try:
        user_start = (float(request.args.get('user_start_lat')), float(request.args.get('user_start_lng')))
        station_start = (float(request.args.get('station_start_lat')), float(request.args.get('station_start_lng')))
        station_end = (float(request.args.get('station_end_lat')), float(request.args.get('station_end_lng')))
        user_end = (float(request.args.get('user_end_lat')), float(request.args.get('user_end_lng')))
    except (TypeError, ValueError):
        return jsonify({'error': 'Coordonnées invalides ou manquantes'}), 400

    # 1. Le début à pied jusqu'à la station
    path1 = get_ors_route(user_start[0], user_start[1], station_start[0], station_start[1], 'foot-walking')
    
    # 2. Le trajet en vélo entre les deux stations
    path2 = get_ors_route(station_start[0], station_start[1], station_end[0], station_end[1], 'cycling-regular')
    
    # 3. La fin à pied jusqu'à l'arrivée
    path3 = get_ors_route(station_end[0], station_end[1], user_end[0], user_end[1], 'foot-walking')

    def extract_summary(path):
        """Extrait durée (s) et distance (m) depuis un GeoJSON ORS."""
        if not path:
            return None
        try:
            summary = path['features'][0]['properties']['summary']
            return {
                'duration': round(summary.get('duration', 0)),
                'distance': round(summary.get('distance', 0))
            }
        except Exception:
            return None

    summary1 = extract_summary(path1)
    summary2 = extract_summary(path2)
    summary3 = extract_summary(path3)

    return jsonify({
        'path1': path1,
        'path2': path2,
        'path3': path3,
        'summary1': summary1,
        'summary2': summary2,
        'summary3': summary3,
    })

# APIs stations JCDecaux 
@app.route('/api/getBikesAround')
def get_bikes_around():
    # on recup la ville qu'on a choisi dans le menu
    contract = request.args.get('contract')
    
    lat_user = request.args.get('lat', type=float)
    lng_user = request.args.get('lng', type=float)
    mode = request.args.get('mode') # si 'start' on cherche velos dispo, si 'end' on cherche places dispo

    if not contract:
        return jsonify({'error': 'faut choisir une ville frrr'}), 400
    if not JCDECAUX_API_KEY:
        return jsonify({'error': 'pas de clé api '}), 500

    # requete vers l'api jcdecaux
    url = f'https://api.jcdecaux.com/vls/v1/stations?contract={contract}&apiKey={JCDECAUX_API_KEY}'
    print(f"Appel JCDecaux: {url.replace(JCDECAUX_API_KEY, 'HIDDEN')}") # juste pour check dans la console
    try:
        r = requests.get(url, timeout=10) 
        if r.status_code != 200:
            print(f"Erreur retour JCDecaux: {r.status_code} - {r.text}") # ça a planté, on log
        r.raise_for_status()
        data = r.json()
        
        # faut que ce soit une liste sinon c'est pas normal
        if not isinstance(data, list):
             print(f"WTF format received: {data}")
             return jsonify({'error': 'Format de données chelou'}), 500

        # on filtre un peu tout ce bordel
        stations = []
        for s in data:
            pos = s.get('position')
            if not isinstance(pos, dict): 
                
                lat = s.get('latitude')
                lng = s.get('longitude')
            else:
                lat = pos.get('lat')
                lng = pos.get('lng')

            if lat is None or lng is None:
                continue

            available_bikes = s.get('available_bikes', 0)
            available_stands = s.get('available_bike_stands', 0)
            status = s.get('status', 'CLOSED')
            
            # Si c'est fermé ça degage
            if status != 'OPEN':
                continue
            
            # On recupère la distance pour trier après
            dist = 0
            if lat_user and lng_user:
                dist = get_distance_km(lat_user, lng_user, lat, lng)
            
            stations.append({
                'name': s.get('name'),
                'address': s.get('address'),
                'lat': lat,
                'lng': lng,
                'available_bikes': available_bikes, 
                'bike_stands': s.get('bike_stands', 0), 
                'available_bike_stands': available_stands, 
                'status': status,
                'distance': dist
            })
            
        # Maintenant on trie par distance
        if lat_user and lng_user:
            stations.sort(key=lambda x: x['distance'])
            
            selected_stations = []
            valid_count = 0
            
            # On prend les meilleures stations selon le mode (depart ou arrivee)
            for s in stations:
                is_valid = False
                if mode == 'start':
                    if s['available_bikes'] > 0:
                         valid_count += 1
                elif mode == 'end':
                    if s['available_bike_stands'] > 0:
                         valid_count += 1
                else: 
                     # mode pas definie, on prend tout
                     valid_count += 1
                
                selected_stations.append(s)
                
                # On en garde que 3 ça suffit large
                if valid_count >= 3:
                    break
            
            stations = selected_stations
            
        return jsonify({'stations': stations}) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # gestion d'erreur basique

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) # go lancer le bouzin
