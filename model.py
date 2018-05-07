"""Models and databases for users and accounts"""

from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


##############################################################################
# Part 1: Compose ORM

class Daily_Input(db.Model):
    """Daily behavior and well-being model"""

    __tablename__ = "daily_inputs"

    input_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey('users.user_id'), nullable=False)
    sleep = db.Column(db.Integer, nullable=False)
    exercise = db.Column(db.Integer, nullable=False)
    screen_time = db.Column(db.Integer, nullable=False)
    well_being_rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Date: %d user_id: %s sleep: %s exercise: %s screen time: %s>",
         "well_being_rating: %s>" % (self.date, self.user_id, self.sleep, self.exercise, self.screen_time, self.well_being_rating)


class User(db.Model):
    """User model"""

    __tablename__ = "users"


    user_id = db.Column(db.String(30), primary_key=True, nullable=False)
    password = db.Column(db.Strubg(15), nullable=False)
    name = db.Column(db.String(15), nullable=False)
    account_created_on = db.Column(db.DateTime), nullable=False)


    def __repr__(self):
        return "<User_id: %S Password: %s Name: %s Account created:%s>\n" % (self.user_id, 
            self.password, self.name, self.account_created_on)


##############################################################################
# work on later

# def init_app():
#     from flask import Flask
#     app = Flask(__name__)

#     connect_to_db(app)
#     print "Connected to DB."


# def connect_to_db(app):
#     """Connect the database to our Flask app."""

#     app.config['SQLALCHEMY_DATABASE_URI'] = #fix later
#     app.config['SQLALCHEMY_ECHO'] = False
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.app = app
#     db.init_app(app)


# if __name__ == "__main__":


#     init_app()
