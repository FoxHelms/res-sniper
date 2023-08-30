import requests as r
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import text
from find_venue_id import get_venue_id
from controller import get_rest_from_user as convertString
from logincred import login_data
from os import path
from cryptic import *

app = Flask(__name__)
#app.register_blueprint(views,url_prefix='/')


# Database init
db = SQLAlchemy()
db_name = 'restaurants.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey'
#  Add this to work within application context
app.app_context().push()
db.init_app(app)




def create_database():
    if not path.exists('instance/' + db_name):
        with app.app_context():
            db.create_all()
            db.session.commit()
        print('Created Databases!')

def tryLogin(data):
    hdrs = {
    'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
    'Origin': 'https://resy.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }




    post_path = 'https://api.resy.com/3/auth/password'

    return r.post(post_path, headers=hdrs, data=data)





class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restName = db.Column(db.String(200), nullable=False)
    venId = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # db.session.commit()
    # db.session.close()

    def __repr__(self):
        return '<Restaurant %r>' % self.id




create_database()


@app.route('/', methods=['GET', 'POST'])
def home():
    if not login_data:
       return redirect('/login')
    if request.method == 'POST':
        # bot = resbot.ResBot()
        userRest = request.form['userRest']
        convStr = convertString(userRest)
        venue_id = get_venue_id(convStr)
        new_rest = Restaurants(restName=userRest, venId=venue_id)
        #mdb.write_to_db(userRest,venue_id)
        try:
            db.session.add(new_rest)
            db.session.commit()
            # db.session.close()
            return redirect('/')
        except:
            return 'There was an issue adding your restaurant'
    else:
        restaurants = Restaurants.query.order_by(Restaurants.date_created).all()
        return render_template('index.html', restaurants=restaurants)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # bot = resbot.ResBot()
        ResyEmail = request.form['ResyEmail']
        ResyPW = request.form['ResyPW']
        data = {'email': ResyEmail, 'password': ResyPW}
        result = tryLogin(data)
        if result.status_code != 200:
            return render_template('error.html', message='Please login using your Resy credentials', e_code=result.status_code)
        else:
            with open('logincred.py', 'w') as lic:
                enc_user = encrypt_message(ResyEmail)
                enc_pw = encrypt_message(ResyPW)
                creds_to_write = 'login_data = {"email" : ' + '"' + str(enc_user) + '"' + ', "password" :  ' + '"' + str(enc_pw) + '"' + '}'
                lic.write(creds_to_write)
                lic.close()
            return redirect('/')
    else:
        return render_template('login.html')


@app.route('/delete/<int:id>')
def delete(id):
    rest_to_delete = Restaurants.query.get_or_404(id)

    try:
        db.session.delete(rest_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return render_template('error.html', message='There was a problem deleting your restaurant', e_code='Please Try Again')


@app.route('/error', methods=['GET','POST'])
def error(message, e_code):
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template('errors.html', message=message, e_code=e_code)



def cantestdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

if __name__ == '__main__':
    #mdb.create_table()
    app.run(debug=True)
    
    