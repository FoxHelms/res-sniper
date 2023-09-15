import requests as r
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import path
from cryptic import *
from resbot import RestaurantIdentifier
from check_url import conf_good_url
from logincred import login_data

app = Flask(__name__)

# Database init
db = SQLAlchemy()
db_name = 'restaurants.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey'
db.init_app(app)


def create_database():
    '''Check for database and create one in app context'''
    if not path.exists('instance/' + db_name):
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
    return r.post(post_path, headers=hdrs, data=data)

class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restName = db.Column(db.String(200), nullable=False)
    venId = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Restaurant %r>' % self.id

create_database()


@app.route('/', methods=['GET', 'POST'])
def home():
    '''
    Home, defaults to login, maintains list, adds ven IDs to db
    '''
    if not login_data:
       return redirect('/login')
    if request.method == 'POST':
        userRest = request.form['userRest']
        if not conf_good_url(userRest):
            return render_template('error.html', message='Please enter a resy restaurant link', e_code='Please Try Again')
        venue_id = RestaurantIdentifier.get_venue_id(userRest)
        new_rest = Restaurants(restName=userRest, venId=venue_id)
        try:
            db.session.add(new_rest)
            db.session.commit()
            return redirect('/')
        except:
            return render_template('error.html', message='There was a problem adding your restaurant', e_code='Please Try Again')
    else:
        restaurants = Restaurants.query.order_by(Restaurants.date_created).all()
        return render_template('index.html', restaurants=restaurants)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login page, tries login with user input
    '''
    if request.method == 'POST':
        ResyEmail = request.form['ResyEmail']
        ResyPW = request.form['ResyPW']
        data = {'email': ResyEmail, 'password': ResyPW}
        result: r.models.Response = tryLogin(data)
        if result.status_code != 200:
            return render_template('error.html', message='Please login using your Resy credentials', e_code=result.status_code)
        else:
            with open('logincred.py', 'w') as lic:
                # Stores encrypted data to protect user data
                enc_user = encrypt_message(ResyEmail) 
                enc_pw = encrypt_message(ResyPW)
                dic_data = {'email' : enc_user, 'password' :  enc_pw}
                creds_to_write = f'login_data = {dic_data}'
                lic.write(creds_to_write)
                lic.close()
            return redirect('/')
    else:
        return render_template('login.html')


@app.route('/delete/<int:id>')
def delete(id):
    '''
    Delete, removecs rest from database
    '''
    rest_to_delete = Restaurants.query.get_or_404(id)
    try:
        db.session.delete(rest_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return render_template('error.html', message='There was a problem deleting your restaurant', e_code='Please Try Again')


@app.route('/error', methods=['GET','POST'])
def error(message, e_code):
    '''
    Error page, shows message and error code, redirects to home page'''
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template('errors.html', message=message, e_code=e_code)

if __name__ == '__main__':
    app.run(debug=True)
    
    