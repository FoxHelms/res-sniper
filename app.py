from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import text
from views import views
import resbot
from controller import get_rest_from_user as convertString



app = Flask(__name__)
#app.register_blueprint(views,url_prefix='/')


# Database init
db = SQLAlchemy()
db_name = 'restaurants.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)


bot = resbot.ResBot()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        userRest = request.form['userRest']
        convStr = convertString(userRest)
        venue_id = bot.get_venue_id(convStr)
    else:
        venue_id = ''

    return render_template('index.html', venue_id=venue_id)


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