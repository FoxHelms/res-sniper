from flask import Blueprint, render_template, url_for, request, redirect
import resbot
from controller import get_rest_from_user as convertString

views = Blueprint(__name__,'views')
bot = resbot.ResBot()

@views.route('/')
def home():
    if request.method == 'POST':
        userRest = request.form['userRest']
        convStr = convertString(userRest)
        venue_id = bot.get_venue_id(convStr)
    else:
        venue_id = ''

    return render_template('index.html', venue_id=venue_id)