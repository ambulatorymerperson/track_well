"""Models and databases for users and accounts"""

from flask_sqlalchemy import SQLAlchemy
import time
from datetime import date, timedelta
# how to use datetime : http://www.pythonforbeginners.com/basics/python-datetime-time-examples

# >>> print datetime.date.today().strftime("%B")
# May
# >>> print datetime.date.today().strftime("%d")
# 08
# >>> print datetime.date.today().strftime("%Y")
# 2018

# >>> datetime.datetime.now().strftime("%m-%d-%y")
# '05-08-18'

db = SQLAlchemy()


##############################################################################
# Part 1: Compose ORM

class Daily_Input(db.Model):
    """Daily behavior and well-being model"""

    __tablename__ = "daily_inputs"

    input_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime(15), nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey('users.ID'), nullable=False)
    sleep = db.Column(db.Float, nullable=False)
    exercise = db.Column(db.Float, nullable=False)
    screen_time = db.Column(db.Float, nullable=False)
    well_being_rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Input ID: {} Date: {} user_id: {} sleep: {} exercise: {} screen time: {} well_being_rating: {}>".format(self.input_id, self.date, self.user_id, self.sleep, self.exercise, self.screen_time, self.well_being_rating)


class User(db.Model):
    """User model"""

    __tablename__ = "users"


    ID = db.Column(db.String(30), primary_key=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(15), nullable=False)
    first_entry_at = db.Column(db.DateTime(15), nullable=True)


    def __repr__(self):
        return "<User_id: {} Password: {} Name: {} Started tracking on:{}>\n".format(self.ID, self.password, self.name, self.first_entry_at)

class Custom_Variable_Daily_Entry(db.Model):
    """ A table for keeping track of each entries for user-generated custom variables """

    __tablename__ = "custom_variable_dailies"

    input_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    variable_info = db.Column(db.Integer, db.ForeignKey('custom_variable_info.variable_id'), nullable=False)
    daily_default_v_input_id = db.Column(db.Integer, db.ForeignKey('daily_inputs.input_id'), nullable=False)
    custom_variable_amount = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return "<Input id: {} Variable Info: {} Default Variable Input ID: {} Custom Variable Amount:{}>\n".format(self.input_id, self.variable_info, self.daily_default_v_input_id, self.custom_variable_amount)

class Custom_Variable_Info(db.Model):
    """ A table that holds all the information for custom independnet variables designed by users """

    __tablename__ = "custom_variable_info"

    variable_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String(15), db.ForeignKey('users.ID'), nullable=False)
    variable_name = db.Column(db.String(20), nullable=False)
    variable_units = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<Variable id: {} User id: {} Variable name: {} Variable units:{}>\n".format(self.variable_id, self.user_id, self.variable_name, self.variable_units)


##############################################################################
def example_data():
    """sample data for test"""

    ly = User(ID="Leroy", password="bad", name="Brown")

    db.session.add(ly)
    db.session.commit()
    
    jan1 = Daily_Input(date=date.today(), user_id="Leroy", sleep=4, exercise=3, screen_time=0, well_being_rating=5)
    jan2 = Daily_Input(date=date.today() - timedelta(1), user_id="Leroy", sleep=10, exercise= 4, screen_time=0, well_being_rating=4)
    jan3 = Daily_Input(date=date.today() - timedelta(2), user_id="Leroy", sleep= 6, exercise=1, screen_time=0, well_being_rating=3)
    jan4 = Daily_Input(date=date.today() - timedelta(3), user_id="Leroy", sleep=7.5, exercise=2, screen_time=0, well_being_rating=4)
    jan5 = Daily_Input(date=date.today() - timedelta(4), user_id="Leroy", sleep=10, exercise=0, screen_time=0, well_being_rating=4)



    db.session.add_all([jan1, jan2, jan3, jan4, jan5])
    db.session.commit()

def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app, db_uri="postgresql:///track_well"):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":


    init_app()
