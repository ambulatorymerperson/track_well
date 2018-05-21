"""Models and databases for users and accounts"""

from flask_sqlalchemy import SQLAlchemy
import time
import datetime
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
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey('users.ID'), nullable=False)
    sleep = db.Column(db.Float, nullable=False)
    exercise = db.Column(db.Float, nullable=False)
    screen_time = db.Column(db.Float, nullable=False)
    well_being_rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Date: {} user_id: {} sleep: {} exercise: {} screen time: {} well_being_rating: {}>".format(self.date, self.user_id, self.sleep, self.exercise, self.screen_time, self.well_being_rating)


class User(db.Model):
    """User model"""

    __tablename__ = "users"


    ID = db.Column(db.String(30), primary_key=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(15), nullable=False)
    first_entry_at = db.Column(db.DateTime, nullable=True)


    def __repr__(self):
        return "<User_id: {} Password: {} Name: {} Started tracking on:{}>\n".format(self.ID, self.password, self.name, self.first_entry_at)


##############################################################################
def example_data():
    """sample data for test"""

    Ly = users(ID="Leroy", password="bad", name="Brown")
    
    jan1 = daily_inputs(date=2018-01-01, user_id="Leroy", sleep=4, exercise=3, screen_time=0, well_being_rating=5)
    jan2 = daily_inputs(date=2018-01-02, user_id="Leroy", sleep=10, exercise= 4, screen_time=0, well_being_rating=4)
    jan3 = daily_inputs(date=2018-01-03, user_id="Leroy", sleep= 6, exercise=1, screen_time=0, well_being_rating=3)
    jan4 = daily_inputs(date=2018-03-17, user_id="Leroy", sleep=7.5, exercise=2, screen_time=0, well_being_rating=4)
    jan5 = daily_inputs(date=2018-03-17, user_id="Leroy", sleep=10, exercise=0, screen_time=0, well_being_rating=4)

    db.session.add_all([Ly, jane1, jan2, jan3, jan4, jan5])
    db.session.commit()

def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///track_well'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":


    init_app()
