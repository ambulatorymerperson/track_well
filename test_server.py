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

    def test_add_info_page(self):
        with self.client as c:
          with c.session_transaction() as sess:
              sess['current_user'] = "Leroy"
        result = self.client.get('/record_daily_input')
        self.assertIn('Record what you did and how you felt yesterday', result.data)                


class WellnessTrackerTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///example_database")

        db.create_all()
        example_data()


    def test_login_and_logout(self):
        result = self.client.post("/login",
                              data={"email_input": "Leroy",
                                    "pw_input": "bad"},
                              follow_redirects=True)
        self.assertIn('Out of all the activities you are tracking', result.data)

        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn('Welcome to track well', result.data)

        result = self.client.post("/login",
                              data={"email_input": "Leroy",
                                    "pw_input": "cheese"},
                              follow_redirects=True)
        self.assertIn('Invalid password. Please try again.', result.data)

        result = self.client.post("/login",
                              data={"email_input": "Heroy",
                                    "pw_input": "cheese"},
                              follow_redirects=True)
        self.assertIn('That email is not in our database. Please check your spelling, or use the form below to register', result.data)

    def test_registration(self):
        result = self.client.post('/register', data={'email_input':'letter@alphabet.words', 'pw_input':'scrtvwls', 'name':'Tony'},
                                    follow_redirects=True)
        self.assertIn('We have your email as letter@alphabet.words', result.data)                                 


    def test_registration_confirmation(self):
        with self.client as c:
          with c.session_transaction() as sess:
              sess['current_user'] = "Leroy"
        result = self.client.get('/registration_confirmation')
        self.assertIn('Welcome, Brown!', result.data)    


    def test_rsquared(self):
        with self.client as c:
          with c.session_transaction() as sess:
              sess['current_user'] = "Leroy"

        result = self.client.get("/my_stats")
        self.assertIn("Out of all the activities you are tracking, exercise is the most relevent to your sense of well-being.", result.data)    

        #sleep r2 should be 0.07409284
        #exercise r2 should be 0.19998784       

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    

if __name__ == "__main__":
    unittest.main()
    
