
from model import User, Daily_Input connect_to_db, db

def calculate_pearson_correlation(user_id, behavior): 
    r = (sum(x) * sum (y))/