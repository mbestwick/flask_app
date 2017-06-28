""" A sample test document """

from unittest import TestCase
from model import connect_to_db, db, example_data
from server import app
from flask import session


class FlaskTestsBasic(TestCase):
    """ Flask tests for the server. """

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn('ENTER TEXT', result.data)


class FlaskTestsDatabase(TestCase):
    """ Flask tests for the database. """

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()


class FlaskTestsLoggedIn(TestCase):
    """ Flask tests with user logged in to session. """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_login(self):
        """ Tests that doesn't let you log in if already logged in. """
        result = self.client.get('/login', follow_redirects=True)
        self.assertIn('ENTER TEXT', result.data)


if __name__ == "__main__":
    import unittest
    unittest.main()
