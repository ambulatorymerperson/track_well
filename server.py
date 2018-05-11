from statistical_functions import calculate_coefficient_of_determination

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context)


from flask_debugtoolbar import DebugToolbarExtension

from model import User, Daily_Input, connect_to_db, db


app = Flask(__name__)


app.secret_key = "ZYX"

@app.route('/')
def show_homepage():
    """show home page"""

    return render_template("homepage.html")




@app.route("/register", methods=["POST"])
def register_process():
    """Registration Form."""

    email_input = request.form['email_input']
    pw_input = request.form['pw_input']

    if User.query.filter_by(email = email_input).all() != []:
        return redirect('/')       
    else:
        new_user = User(ID= ID, password=pw_input)
        db.session.add(new_user)
        db.session.commit() 

    return redirect('/')

@app.route("/login", methods=["POST"])
def login():
    email_input = request.form['email_input']
    pw_input = request.form['pw_input']

    if User.query.filter(User.ID == email_input, User.password == pw_input).all() != []:
        user = User.query.filter(User.ID == email_input).one()
        session['current_user'] = user.ID
        flash('You were successfully logged in')
        return redirect("/my_stats")
    else:
        flash('Your e-mail or password was incorrect! Please try again or Register.')
        return render_template("log_in.html")

@app.route("/my_stats")
def show_user_stats():

    current_user = session['current_user']
    user_stats = Daily_Input.query.filter_by(user_id=current_user).all()
    user = User.query.filter(User.ID == current_user).one()
    name = user.name
    sleep = []
    screentime = []
    exercise = []
    well_being_rating = []

    for info in user_stats:
        sleep += [info.sleep]
        screentime += [info.screen_time]
        exercise += [info.exercise]
        well_being_rating += [info.well_being_rating]
    
   

    return render_template("my_stats.html", sleep=sleep, screentime=screentime, exercise=exercise, well_being_rating=well_being_rating, name=name)

@app.route("/logout")
def logout():
    del session['current_user']


    flash('Happy tracking! Tee hee!')
    return redirect ("/")    

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
