
#from model import User, Daily_Input, connect_to_db, db
from math import sqrt
from scipy import stats
import numpy as np

def calculate_coefficient_of_determination(behavior, wellness):

    slope, intercept, r_value, p_value, std_err = stats.linregress(behavior, wellness)

    print "r-squared: {}".format(r_value**2)
    return r_value**2
    
