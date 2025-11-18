import requests as r
from flask import Flask, session, g, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from resbot import RestaurantIdentifier
from check_url import conf_good_url

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

# Database init
db = SQLAlchemy()
db_name = 'restaurants.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['CACHE_TYPE'] = 'SimpleCache' 
db.init_app(app)
restaurantIdentifier = RestaurantIdentifier()


def create_database():
    '''Check for local database and create one in app context'''
    if not os.path.exists('instance/' + db_name):
        with app.app_context():
            db.create_all()
            db.session.commit()

def tryLogin(data: dict) -> r.models.Response:
    '''Try logging in to Resy with user provided credentials'''
    hdrs: dict = {
        'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
        'Origin': 'https://resy.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    post_path: str = 'https://api.resy.com/3/auth/password'
    return r.post(post_path, headers=hdrs, json=data)

class Restaurants(db.Model):
    ''' Table class for restaurants database'''
    id = db.Column(db.Integer, primary_key=True)
    restName = db.Column(db.String(200), nullable=False)
    venId = db.Column(db.Integer)
    venUrl = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Restaurant %r>' % self.id

create_database()


USER_DATA = {
    "username": "testuser",
    "password": "password123"
}

@app.route('/api/login', methods=['POST'])
def login_api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
        ResyEmail = data.get('ResyEmail')
        ResyPW = data.get('ResyPW')

        if not ResyEmail or not ResyPW:
            return jsonify({"error": "Email and password required"}), 400

        session.pop('user', None)
        session.pop('passw', None)

        result = tryLogin({"email": ResyEmail, "password": ResyPW})

        if result.status_code != 200:
            try:
                error_data = result.json()  # Try parsing JSON
            except ValueError:
                error_data = result.text  # Fallback to raw text
            return jsonify({"error": error_data}), 400

        # Try parsing JSON safely for success case
        try:
            page_json = result.json()
        except ValueError:
            return jsonify({"error": "Unexpected response format"}), 500

        # Save auth token
        with open('auth_token.txt', 'w') as f:
            f.write(page_json.get('token', '') + '\n')
            f.write('{"id":' + str(page_json.get('payment_method_id', '')) + '}')

        session['user'] = ResyEmail
        session['passw'] = ResyPW

        return jsonify({"message": "Login successful"}), 200
    except Exception as e:
        print("Login API exception:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/api/restaurants', methods=['GET', 'POST'])
def restaurants_api():
    if not g.user:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'POST':
        userUrl = request.json.get('userRest')
        if not conf_good_url(userUrl):
            return jsonify({"error": "Invalid Resy URL"}), 400

        lower_name_rest = restaurantIdentifier.convert_url(userUrl)[1].replace('-', ' ')
        name_rest = lower_name_rest.title()
        venue_id = restaurantIdentifier.get_venue_id(userUrl)
        new_rest = Restaurants(restName=name_rest, venId=venue_id, venUrl=userUrl)

        try:
            db.session.add(new_rest)
            db.session.commit()
            return jsonify({"message": "Restaurant added"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        restaurants = Restaurants.query.order_by(Restaurants.date_created).all()
        rest_list = [
            {"id": r.id, "restName": r.restName, "venUrl": r.venUrl}
            for r in restaurants
        ]
        return jsonify(rest_list)


@app.route('/api/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant_api(id):
    rest_to_delete = Restaurants.query.get_or_404(id)
    try:
        db.session.delete(rest_to_delete)
        db.session.commit()
        return jsonify({"message": "Deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/me', methods=['GET'])
def me():
    if 'user' in session:
        return jsonify({"loggedIn": True, "email": session['user']})
    else:
        return jsonify({"loggedIn": False})

@app.route('/error', methods=['GET','POST'])
def error(message, e_code):
    '''
    Error page, shows message and error code, redirects to home page'''
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template('errors.html', message=message, e_code=e_code)


@app.before_request
def before_request():
    g.user = None
    if 'user' in session and 'passw' in session:
        g.user = session['user']
        g.passw = session['passw']


if __name__ == '__main__':
    app.run(debug=True)
    
    