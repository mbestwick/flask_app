""" A sample db model. """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

###############################################################################
# MODEL DEFINITIONS


class User(db.Model):
    """ A user of the site. """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User %s: %s>' % (self.user_id, self.username)


def connect_to_db(app, db_uri='postgresql:///DATABASENAME'):
    """ Connects the database to the Flask app. """

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    db.app = app
    db.init_app(app)

###############################################################################
# HELPER FUNCTIONS


def example_data():
    """ Creates sample data for testing. """
    user1 = User()
    user2 = User()

    db.session.add_all([user1, user2])
    db.session.commit()


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
