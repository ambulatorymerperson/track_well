from statistical_functions import calculate_coefficient_of_determination

from jinja2 import StrictUndefined

from math import (sqrt, modf)
from scipy import stats
import numpy as np


from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context, json)


from flask_debugtoolbar import DebugToolbarExtension

from datetime import date, timedelta

from model import User, Daily_Input, connect_to_db, db


app = Flask(__name__)


app.secret_key = "ZYX"

regression_info = {}

next_day_regression_info = {}

@app.route('/')
def show_homepage():
    """show home page"""

    return render_template("homepage.html")




@app.route("/register", methods=["POST"])
def register_process():
    """Registration Form."""

    email_input = request.form['email_input']
    pw_input = request.form['pw_input']
    name = request.form['name']

    if User.query.filter_by(ID == email_input).all() != []:
        flash('That email is already attached to an account.')
        return redirect('/')       
    else:
        new_user = User(ID = email_input, password=pw_input, name=name)
        db.session.add(new_user)
        db.session.commit()
        session['current_user'] = email_input 

    return redirect('/registration_confirmation')

@app.route("/registration_confirmation")
def confirm_registration():

    if 'current_user' not in session:
        return redirect('/')

    user_email = session['current_user']
    user = User.query.filter(User.ID == user_email).one()
    name = user.name
    password = user.password    

    return render_template("registration_confirmation.html", name=name, password=password)

@app.route("/login", methods=["POST"])
def login():
    email_input = request.form['email_input']
    pw_input = request.form['pw_input']

    if User.query.filter(User.ID == email_input, User.password == pw_input).all() != []:
        user = User.query.filter(User.ID == email_input).one()
        session['current_user'] = user.ID
        return redirect("/my_stats")
    elif User.query.filter(User.ID == email_input).all() == []:
        flash('That email is not in our database. Please check your spelling, or use the form below to register', 'error')
        return redirect("/")
    elif User.query.filter(User.ID == email_input, User.password == pw_input).all()  == []:
        flash('Invalid password. Please try again.', 'error')
        return redirect("/")    


@app.route("/my_stats")
def show_user_stats():

    if 'current_user' not in session:
        flash('Please log in first')
        return redirect('/')

    current_user = session['current_user']
    user_stats = Daily_Input.query.filter_by(user_id=current_user).order_by('date').all()

    if len(user_stats) < 1:
        flash('You have not entered any data yet. Please enter data in order to view behavioral graphs.')
        return redirect("/record_daily_input")

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

    
    sleep_r = []
    screentime_r = []
    exercise_r = []

    regression_lines = [sleep_r, screentime_r, exercise_r]
    independent_variables = [sleep, screentime, exercise]

    sleep_points, screen_points, exercise_points = find_next_day_effects(independent_variables, well_being_rating)

    next_day_plot_points = [sleep_points, screen_points, exercise_points]

    next_day_regression_info = create_regression_dict(next_day_plot_points, sleep_points, screen_points, exercise_points)

    # goes through each item in each independent variable list and pairs it with its corresponding
    # wellness score. The item and the wellness score become a sublist, which is appended to a 
    # list in regression lines. Because this loop simulatenously goes through regression_lines
    # and independent_variables, sleep_r uses data from sleep, screentime_r uses data from screentime, etc.
    for j in range(len(independent_variables)) and range(len(regression_lines)):
        for i in range(len(independent_variables[j])) and range(len(well_being_rating)):
            regression_lines[j].append([independent_variables[j][i], well_being_rating[i]])

    # for i in range(len(sleep)) and range(len(well_being_rating)):
    #     sleep_r.append([sleep[i], well_being_rating[i]])

    # for i in range(len(screentime)) and range(len(well_being_rating)):
    #     screentime_r.append([screentime[i], well_being_rating[i]])

    # for i in range(len(exercise)) and range(len(well_being_rating)):
    #     exercise_r.append([exercise[i], well_being_rating[i]])

    

    

    for lst in independent_variables:    
        slope, intercept, r_value, p_value, std_err = stats.linregress(lst, well_being_rating)
        sub_dict = {'slope': slope, 'intercept': intercept, 'r_value': r_value, 'p_value': p_value, 'std_err': std_err}
        if lst == sleep:
            regression_info["sleep"] = sub_dict
        elif lst == screentime:
            regression_info["screentime"] = sub_dict
        elif lst == exercise:
            regression_info["exercise"] = sub_dict
        

    for key in list(regression_info.keys()):
        for lst in independent_variables:
            if key == "sleep" and lst == sleep:
                add_regression_info_to_dict(regression_info, key, lst, len(lst))
            if key == "screentime" and lst == screentime:
                add_regression_info_to_dict(regression_info, key, lst, len(lst))
            if key == "exercise" and lst == exercise:
                add_regression_info_to_dict(regression_info, key, lst, len(lst))

    for key in list(next_day_regression_info.keys()):
        for lst in next_day_plot_points:
            if key == "sleep" and lst == sleep_points:
                add_regression_info_to_dict(next_day_regression_info, key, lst, len(lst))
            if key == "screen" and lst == screen_points:
                add_regression_info_to_dict(next_day_regression_info, key, lst, len(lst))
            if key == "exercise" and lst == exercise_points:
                add_regression_info_to_dict(next_day_regression_info, key, lst, len(lst))              

    ordered_ars = determine_relevence_of_behavior(regression_info)

    most_relevent_activity = "behavior"

    for behavior in regression_info:
        if regression_info[behavior]["adjusted_r_squared"] == ordered_ars[-1]:
            most_relevent_activity = behavior

    biggest_next_day_impact = "behavior"

    next_day_sorted_ars = determine_relevence_of_behavior(next_day_regression_info)

    for behavior in next_day_regression_info:
        if next_day_regression_info[behavior]["adjusted_r_squared"] == next_day_sorted_ars[-1]:
            biggest_next_day_impact = behavior

    next_day_insight = "stuff"
            
    if next_day_regression_info[biggest_next_day_impact]["slope"] < 0:
        next_day_insight = "the less {} you get, the better you tend to feel the next day.".format(biggest_next_day_impact)
    elif next_day_regression_info[biggest_next_day_impact]["slope"] > 0:
        next_day_insight = "the more {} you get, the better you tend to feel the next day.".format(biggest_next_day_impact)

    same_day_insight = "stuff"

    if regression_info[most_relevent_activity]["slope"] < 0:
        same_day_insight = "the less {} you get, the better you tend to feel that day.".format(most_relevent_activity)
    elif regression_info[most_relevent_activity]["slope"] > 0:
        same_day_insight = "the more {} you get, the better you tend to feel that day.".format(most_relevent_activity)        

    same_day_message = "Out of all the activities you are tracking, {} is the most relevent to your sense of well-being that day. {}".format(most_relevent_activity, same_day_insight)    
    
    return render_template("my_stats.html", sleep=sleep_r, screentime=screentime_r, exercise=exercise_r, name=name, independent_variables=independent_variables, regression_info=regression_info, ordered_ars=ordered_ars, sleep_points=sleep_points, screen_points=screen_points, exercise_points=exercise_points, biggest_next_day_impact=biggest_next_day_impact, next_day_insight=next_day_insight, same_day_message=same_day_message)             
                 
# key refers to keys in regression_info dictionary. These keys share the same name as the lists in the
# independent variable list, because the dictionary info is based on these lists
def add_regression_info_to_dict(dictionary, key, lst, n):
    """Calculate adjusted r squared for each data set of dependent + independent variables, and add it to the data set dict."""    
# n is the sample size
# adjusted_r_squared formula used can be found here: http://mtweb.mtsu.edu/stats/dictionary/formula.htm   
    dictionary[key]['n'] = len(lst)
    r_value = dictionary[key]['r_value']
# I hardcoded k to 1 because for the first chart, each scatter plot and regression line is for 1
# independent variable (k is supposed to be number of independent variables).    
    adjusted_r_squared = 1 - (((1 - r_value**2) * (n-1))/(n-1-1))
    dictionary[key]['adjusted_r_squared'] = adjusted_r_squared

def determine_relevence_of_behavior(dictionary):
    """Pass in the dict with all the regression info and see which behaviors are most relevent to the user.
    Return print statements that provide correlative insights."""

    highest_influences = []

    for behavior in dictionary:
        r = dictionary[behavior]["adjusted_r_squared"]
        highest_influences.append(r)

    return sorted(highest_influences)    

def find_next_day_effects(indep_v_list, wellness_scores):

    sleep_points = []
    screen_points = []
    exercise_points = []

    plot_points_for_next_day_effects = [sleep_points, screen_points, exercise_points]

    for j in range(len(indep_v_list)) and range(len(plot_points_for_next_day_effects)):
        for i in range(len(indep_v_list[j])) and range(len(wellness_scores)-1):
            plot_points_for_next_day_effects[j].append([indep_v_list[j][i], wellness_scores[i+1]])

    return plot_points_for_next_day_effects[0], plot_points_for_next_day_effects[1], plot_points_for_next_day_effects[2]        

def create_regression_dict(lst, sublist_1, sublist_2, sublist_3):
        for item in lst:
            print item     
            slope, intercept, r_value, p_value, std_err = stats.linregress(item)
            sub_dict = {'slope': slope, 'intercept': intercept, 'r_value': r_value, 'p_value': p_value, 'std_err': std_err}
            if item == sublist_1:
                next_day_regression_info["sleep"] = sub_dict
            elif lst == sublist_2:
                next_day_regression_info["screen"] = sub_dict
            elif lst == sublist_3:
                next_day_regression_info["exercise"] = sub_dict 

        return next_day_regression_info           
    

@app.route("/record_daily_input")
def record_input():

    if 'current_user' not in session:
        return redirect('/')

    current_user = session['current_user']
    user = User.query.filter(User.ID == current_user).one()
    name = user.name




    return render_template("record_daily_input.html", name=name)


@app.route("/add_info", methods=["POST"])    
def add_info():

    current_user = session['current_user']

    yesterday = date.today() - timedelta(1)
    if Daily_Input.query.filter(Daily_Input.date==yesterday, Daily_Input.user_id == current_user).all() != []:
        flash('Sorry, you have already entered information for this day. If you believe this information was entered incorrectly, you can change it below.')
        return redirect('/see_all_records')

    sleep_h = request.form.get('sleep_h')
    sleep_m = request.form.get('sleep_m')
    exercise_h =  request.form.get('exercise_h')
    exercise_m = request.form.get('exercise_m')
    screentime_h = request.form.get('screentime_h')
    screentime_m = request.form.get('screentime_m')
    wellness_score = request.form.get('wellness_score')
    



    sleep_t = round((float(sleep_m)/60.0) + float(sleep_h), 2)
    exercise_t = round((float(exercise_m)/60.0) + float(exercise_h), 2)
    screentime_t = round((float(screentime_m)/60.0) + float(screentime_h), 2)

    wellness_score = int(wellness_score)

    new_day_log = Daily_Input(date=yesterday, user_id=current_user, sleep=sleep_t, exercise=exercise_t, screen_time=screentime_t, well_being_rating=wellness_score)
    db.session.add(new_day_log)
    db.session.commit()

    return redirect('/my_stats')

@app.route("/change_row_in_daily_inputs", methods=["POST"])
def change_records():


    current_user = session['current_user']

    date = request.form.get('date') 
    sleep_h = request.form.get('sleep_hours')
    sleep_m = request.form.get('sleep_minutes')
    exercise_h = request.form.get('exercise_hours')
    exercise_m = request.form.get('exercise_minutes')
    screentime_h = request.form.get('screentime_hours')
    screentime_m = request.form.get('screentime_minutes')
    wellness_score = request.form.get('wellness_score')
    entry_number = request.form.get('change_entry_number')

    print "\n\n\n"
    print date
    print "\n\n\n"
    print sleep_h
    print "\n\n\n"
    print sleep_m
    print "\n\n\n"
    print entry_number
    print "\n\n\n\n\n\n"

    entry_number = int(entry_number) - 1
    all_info = Daily_Input.query.filter_by(user_id=current_user).order_by('date').all()
    entry_to_change = all_info[entry_number]
    print entry_to_change
    db.session.delete(entry_to_change)
    db.session.commit()
    # wrong_entry = entry_to_change.input_id
    # deletion = daily_inputs.delete(daily_inputs.input_id == wrong_entry)
    # deletion.execute()

    sleep_t = round((float(sleep_m)/60.0) + float(sleep_h), 2)
    exercise_t = round((float(exercise_m)/60.0) + float(exercise_h), 2)
    screentime_t = round((float(screentime_m)/60.0) + float(screentime_h), 2)

    new_day_log = Daily_Input(date=date, user_id=current_user, sleep=sleep_t, exercise=exercise_t, screen_time=screentime_t, well_being_rating=wellness_score)
    db.session.add(new_day_log)
    db.session.commit()
    flash('entry successfully changed!')
    return redirect('/see_all_records')

@app.route("/see_all_records")
def see_all_records():
    if 'current_user' not in session:
        return redirect('/')

    current_user = session['current_user']

    user = User.query.filter(User.ID == current_user).one()
    name = user.name

    all_info = Daily_Input.query.filter_by(user_id=current_user).order_by('date').all()

    all_entries = []

    for entry in all_info:
        input_dictionary = {}
        input_dictionary['date'] = entry.date
        input_dictionary['sleep'] = "{} hours {} minutes".format(hours_and_minutes(entry.sleep)[0], hours_and_minutes(entry.sleep)[1])
        input_dictionary['exercise'] = "{} hours {} minutes".format(hours_and_minutes(entry.exercise)[0], hours_and_minutes(entry.exercise)[1])
        input_dictionary['screentime'] = "{} hours {} minutes".format(hours_and_minutes(entry.screen_time)[0], hours_and_minutes(entry.screen_time)[1])
        input_dictionary['well_being_rating'] = entry.well_being_rating
        all_entries.append(input_dictionary)

    last_30_days = []
    for i in range(31):
        last_30_days.append(date.today() - timedelta(i))

    length = len(all_entries)    

    return render_template("all_entries.html", all_entries=all_entries, current_user=current_user, length=length, last_30_days=last_30_days, name=name)    
    
def hours_and_minutes(x):

    minutes, hours = modf(x)

    minutes *= 60

    return int(hours), int(minutes)



# @app.route("/check_info")
# def check_info():  
#     current_user = session['current_user']

#     sleep_h = request.args.get('sleep_h', '')
#     sleep_m = request.args.get('sleep_m')
#     exercise_h =  request.args.get('exercise_h')
#     exercise_m = request.args.get('exercise_m')
#     screentime_h = request.args.get('screentime_h')
#     screentime_m = request.args.get('screentime_m')
#     wellness_score = request.args.get('wellness_score')
#     yesterday = date.today() - timedelta(1)



#     sleep_t = round((float(sleep_m)/60) + float(sleep_h), 2)
#     exercise_t = round((float(exercise_m)/60) + float(exercise_h), 2)
#     screentime_t = round((float(screentime_m)/60) + float(screentime_h), 2)



#     return render_template("confirm_input.html", sleep_h=sleep_h, sleep_m=sleep_m, sleep_t=sleep_t, exercise_h=exercise_h, exercise_m=exercise_m, exercise_t=exercise_t, screentime_h=screentime_h, screentime_m=screentime_m, screentime_t=screentime_t, wellness_score=wellness_score, yesterday=yesterday)     

@app.route("/logout")
def logout():
    del session['current_user']

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
