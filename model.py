
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

class NASDAQNYSE(db.Model):
    """Company information database"""

    __tablename__ = "nasdaqnyse"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)   
    ticker_code = db.Column(db.String(10), nullable=False)
    company_name = db.Column(db.String(50), nullable=False)
    bus_sector = db.Column(db.String(60), nullable=True)
    bus_type = db.Column(db.String(60), nullable=True)

    
    # how to return a redable object
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<NASDAQ ticker_code=%s company_name=%s>" % (self.ticker_code, self.company_name)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nasdaqnyse.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."


