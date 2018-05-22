"""test suite for testing track well's server.py"""


from server import app 
import unittest
from model import db, example_data, connect_to_db


class MyAppIntegrationTestCase(unittest.TestCase):
    """testing Flask server"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        result = self.client.get('/')
        self.assertIn('<h1>Welcome to track well</h1>', result.data)

    def my_stats(self):
        result = self.client.get('/my_stats')
        self.assertIn(' <p>Out of all the activities you are tracking,', result.data)        


class WellnessTrackerTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///example_database")

        db.create_all()
        example_data()

    def test_login(self):
        result = self.client.post("/login",
                              data={"user_id": "Leroy",
                                    "password": "bad"},
                              follow_redirects=True)
        self.assertIn('your sense of well-being', result.data) 

    def test_rsquared(self):

        result = self.client.get("/my_stats", data={"User.ID": "Leroy"},
                                            follow_redirects=True)
        self.assertIn("Out of all the activities you are tracking, sleep is the most relevent to your sense of well-being.", result.data)    

        #sleep r2 should be 0.07409284
        #exercise r2 should be 0.19998784       

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    

if __name__ == "__main__":
    unittest.main()
    
