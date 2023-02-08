from model import db, User, Bloodsugar, Insulin, connect_to_db
from sqlalchemy import create_engine, MetaData, Table, Column, Numeric, Integer, VARCHAR, text
from sqlalchemy.sql.expression import update

eng = create_engine('postgresql:///users', echo = True)
meta = MetaData()
conn = eng.connect

def create_user(email, password, name, min_range, max_range):
    """creating new user"""

    user = User(email=email, password=password, name=name, min_range=min_range, max_range=max_range)

    return user

def create_user_with_defaults(email, password, name):
    """creating new user"""

    user = User(email=email, password=password, name=name, min_range=70, max_range=200)

    return user

def get_user_by_email(email):
    """getting a user by their email"""
    user = User.query.filter(User.email == email).first()
    # print("this is the user details")
    # print(user)

    return user

def create_bloodsugar(user_id, bloodsugar, input_date):
    """creating a bloodsugar"""


    bloodsugar_entry = Bloodsugar(user_id=user_id, bloodsugar=bloodsugar, input_date=input_date)

    return bloodsugar_entry

def create_insulin(user_id, insulin_use, input_date):
    """creating an insulin entry"""

    insulin_entry = Insulin(user_id=user_id, insulin_use=insulin_use, input_date=input_date)

    return insulin_entry

def get_bs_by_user_id(user_id):

    bloodsugar = Bloodsugar.query.filter(Bloodsugar.user_id == user_id).all()
    # print("this is blood sugar entries")
    # print(bloodsugar)

    return bloodsugar

def get_Insulin_by_user_id(user_id):

    insulin = Insulin.query.filter(Insulin.user_id == user_id).all()
    # print("this is blood sugar entries")
    # print(bloodsugar)

    return insulin

def get_bs_by_dates(date):

    result = Bloodsugar.query.filter(Bloodsugar.input_date > date).all()

    return result

def update_min(new_num, id):

    db.session.query(User).\
        filter(User.user_id == id).\
        update({'min_range': new_num})
    db.session.commit()    


def update_max(new_num, id):

    db.session.query(User).\
        filter(User.user_id == id).\
        update({'max_range': new_num})
    db.session.commit() 

def update_name(new_name, id):

    db.session.query(User).\
        filter(User.user_id == id).\
        update({'name': new_name})
    db.session.commit() 

def update_password(new_pass, id):

    db.session.query(User).\
        filter(User.user_id == id).\
        update({'password': new_pass})
    db.session.commit() 

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    app.app_context().push()