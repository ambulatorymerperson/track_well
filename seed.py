from sqlalchemy import func
from model import User
from model import Daily_Input
from datetime import datetime
from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    User.query.delete()

    for row in open("seed_data/u.user"):
        row = row.rstrip()
        ID, password, name, first_entry_at = row.split("|")
        first_entry_at = datetime.strptime(first_entry_at, "%m-%d-%y")

        user = User(ID=ID, password=password, name=name, first_entry_at=first_entry_at)

        db.session.add(user)

    db.session.commit()


def load_inputs():
    """Load inputs from u.input.txt into database."""

    print "Daily inputs"

    Daily_Input.query.delete()


    for row in open("seed_data/u.input.txt"):
        row = row.rstrip()
        input_id, date, user_id, sleep, exercise, screen_time, well_being_rating = row.split("|")

        date = datetime.strptime(date, "%m-%d-%y")
        
        daily_input = Daily_Input(input_id=input_id, date=date, user_id=user_id, sleep=sleep, exercise=exercise, screen_time=screen_time, well_being_rating=well_being_rating)
        db.session.add(daily_input)

    db.session.commit()

def set_val_input_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Daily_Input.input_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('daily_inputs_input_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_inputs()
    set_val_input_id()
