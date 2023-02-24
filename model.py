"""Model for blood sugar tracking"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A users profile"""

    __tablename__ = "users_profile"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String,
                      unique=True,
                      nullable=False)
    password = db.Column(db.Text,
                         nullable=False)
    name = db.Column(db.Integer,
                     nullable=False)
    min_range = db.Column(db.Integer,
                          default=70)
    max_range = db.Column(db.Integer,
                          default=200)
    

    bloodsugar = db.relationship("Bloodsugar", back_populates="user")
    insulin = db.relationship("Insulin", back_populates="user")
    food = db.relationship("Food", back_populates="user")

    def __repr__(self):

        return f"User id: {self.user_id} Email: {self.email} Name: {self.name}"


class Bloodsugar(db.Model):
    """Users blood sugar entries"""

    __tablename__ = "bloodsugars"

    bs_id = db.Column(db.Integer,
                      autoincrement=True,
                      primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users_profile.user_id"))
    bloodsugar = db.Column(db.Integer)
    input_date = db.Column(db.DateTime,
                           nullable=False)

    user = db.relationship("User", back_populates="bloodsugar")

    def __repr__(self):

        return f"Blood sugar: {self.bloodsugar} Date input: {self.input_date}"

class Insulin(db.Model):
    """Users insulin use, if any"""

    __tablename__ = "insulin"

    insulin_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users_profile.user_id"))
    insulin_use = db.Column(db.Integer)
    input_date = db.Column(db.DateTime,
                           nullable=False)

    user = db.relationship("User", back_populates="insulin")

    def __repr__(self):

        return f"Insulin usage: {self.insulin_use} Input date: {self.input_date}"
    
class Food(db.Model):
    """food tracking database, user populates"""

    __tablename__ = "food"

    food_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users_profile.user_id"))
    food_name = db.Column(db.String,
                          nullable=False,
                          unique=True)
    serving_size = db.Column(db.Integer,
                             nullable=False)
    calories = db.Column(db.Integer,
                         nullable=False)
    carbs = db.Column(db.Integer,
                      nullable=False)

    user = db.relationship("User", back_populates="food")

    def __repr__(self):

        return f"Food name: {self.food_name} Serving size: {self.serving_size}"


def connect_to_db(flask_app, db_uri="postgresql:///users", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    app.app_context().push()
    connect_to_db(app, echo=False)