from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import text
import resbot
from controller import get_rest_from_user as convertString
from os import path


app = Flask(__name__)
#app.register_blueprint(views,url_prefix='/')


# Database init
db = SQLAlchemy()
db_name = 'restaurants.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  Add this to work within application context
app.app_context().push()
db.init_app(app)




def create_database():
    if not path.exists('instance/' + db_name):
        db.create_all()
        print('Created Database!')



class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restName = db.Column(db.String(200), nullable=False)
    venId = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Restaurant %r>' % self.id

create_database()

bot = resbot.ResBot()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        userRest = request.form['userRest']
        convStr = convertString(userRest)
        venue_id = bot.get_venue_id(convStr)
        new_rest = Restaurants(restName=userRest, venId=venue_id)
        try:
            db.session.add(new_rest)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your restaurant'
    else:
        restaurants = Restaurants.query.order_by(Restaurants.date_created).all()
        return render_template('index.html', restaurants=restaurants)


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
    app.run(debug=True)
    