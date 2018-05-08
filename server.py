from statistical_functions import calculate_coefficient_of_determination

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context)
#from flask_debugtoolbar import DebugToolbarExtension

from model import User, Daily_Input, connect_to_db, db


app = Flask(__name__)


@app.route('/my_stats')
def calculate_correlations():
    """Show user relationship between their behaviors and sense of wellness."""

    current_user = session['current_user']
    user_info = Daily_Input.query.filter_by(user_id=current_user).all()

    user_info.sleep = sleep
    user_info.screen_time = st 
    user_info.exercise = exercise
    user_info.well_being_rating = wbr 



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
