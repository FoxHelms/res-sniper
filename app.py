import requests as r
from flask import Flask, session, g, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from resbot import RestaurantIdentifier
from check_url import conf_good_url

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database init
db = SQLAlchemy()
db_name = 'restaurants.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['CACHE_TYPE'] = 'SimpleCache' 
db.init_app(app)


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
    return r.post(post_path, headers=hdrs, data=data)

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


@app.route('/', methods=['GET', 'POST'])
def home():
    '''
    Home, defaults to login if login creds is empty (meaning no user data has been stored)
    Checks to make sure user provided url is valid, then pulls restaurant name and ID from resy, adds to db
    '''
    if not g.user:
       return redirect('/login')
    if request.method == 'POST':
        userUrl = request.form['userRest']
        if conf_good_url(userUrl) == False:
           return render_template('error.html', message='Please enter a resy restaurant link', e_code='Please Try Again')
        lower_name_rest = RestaurantIdentifier.convert_url(userUrl)[1].replace('-',' ')
        name_rest = lower_name_rest.title()
        venue_id = RestaurantIdentifier.get_venue_id(userUrl)
        new_rest = Restaurants(restName=name_rest, venId=venue_id, venUrl=userUrl)
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
    Login page, posts user input to resy. 
    If resy login succeeds, auth token is stored in local file
    '''
    if request.method == 'POST':
        session.pop('user', None)
        session.pop('passw', None)
        ResyEmail = request.form['ResyEmail']
        ResyPW = request.form['ResyPW']
        data = {'email': ResyEmail, 'password': ResyPW}
        result: int = tryLogin(data)
        if result.status_code != 200:
            return render_template('error.html', message='Please login using your Resy credentials', e_code=result.status_code)
        page_json = result.json()
        with open('auth_token.txt', 'w') as f:
            f.write(page_json['token'])
            f.write('\n')
            f.write('{"id":' + str(page_json['payment_method_id']) + '}')
        session['user'] = ResyEmail
        session['passw'] = ResyPW
        return redirect(url_for('home'))
    else:
        return render_template('login.html')


@app.route('/delete/<int:id>')
def delete(id):
    '''
    Delete, removes rest from database
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


@app.before_request
def before_request():
    g.user = None
    if 'user' in session and 'passw' in session:
        g.user = session['user']
        g.passw = session['passw']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int('3000'), debug=True)
    
    