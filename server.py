from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import date, timedelta, datetime

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """homepage a use starts at"""

    return render_template('startup.html')

@app.route("/login")
def login_page():
    """takes user to the login page"""

    return render_template("login.html")

@app.route("/signup")
def signup_page():
    """takes user to the sign up page"""

    return render_template("signup.html")

@app.route("/user_login", methods=["POST"])
def login():
    """check if a user is in the system and log them in, flash message 
    if password or email incorrect"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("email or password is incorrect.")

        return redirect("/login")

    else:
        user_name = user.name
        session['email'] = user.email
        flash(f"login successful! Welcome back {user.name}")

    return render_template("homepage.html",
                           name=user_name)

@app.route("/user", methods=["POST"])
def register():
    """check if the user already exists, and if not, create a 
    new account"""

    email = request.form.get("email")
    password = request.form.get("password")
    min_range = request.form.get("min_range")
    max_range = request.form.get("max_range")
    name = request.form.get("name")


    if crud.get_user_by_email(email):
        """if a user exists, tell them and redirect back to sign up page 
        (they can decide to go to login then if they want)"""
        flash("user already exists")

        return redirect("/signup")

    else:
        """if no user with email already exists, then create user."""
        
        if min_range or max_range == '':

            user = crud.create_user_with_defaults(email, password, name)
            db.session.add(user)
            db.session.commit()
            flash("account successfully created! Please login.")

            return redirect("/login")

        else:
            user = crud.create_user(email, password, min_range, max_range, name)

            db.session.add(user)
            db.session.commit()
            flash("account successfully created! Please login.")

            return redirect("/login")
        
@app.route("/create_bs_entry", methods=["POST"])
def create_bs_entry():
    
    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)
    bs_entry = request.form.get("bloodsugar_entry")
    current_date = datetime.now()

    user_name = user.name


    """check if a value was given. If no, then flash message to put in number.
    If yes, then add the blood sugar to table"""
    if bs_entry == '':
        flash('Please enter a value for blood sugar to create entry.')

    else:
        entry = crud.create_bloodsugar(user.user_id, int(bs_entry), current_date)
        flash('entry created successfully')


        db.session.add(entry)
        db.session.commit()

    return render_template("homepage.html",
                           name=user_name)

@app.route("/create_insulin_entry", methods=["POST"])
def create_insulin_entry():
    user_email = session.get('email')
    user = crud.get_user_by_email(user_email)
    insulin_entry = request.form.get("insulin_entry")
    current_date = datetime.now()

    user_name = user.name


    if insulin_entry == '':
        flash('Please enter value for insulin to create entry.')

    else:
        entry = crud.create_insulin(user.user_id, int(insulin_entry), current_date)
        flash('entry created successfully')

        db.session.add(entry)
        db.session.commit()

    return render_template("homepage.html",
                            name=user_name)

@app.route("/data")
def data_page():
    """opens data page"""

    return render_template("data.html")

@app.route("/quotes")
def quotes_responses():
    user_email = session.get('email')
    user = crud.get_user_by_email(user_email)

    min = user.min_range
    max = user.max_range

    

@app.route("/entries")
def get_entries():

    user_email = session.get('email')
    user = crud.get_user_by_email(user_email)
    # print("get user by email ran")
    # print(user)
    
    bs_entries = crud.get_bs_by_user_id(user.user_id)
    # print("get bs by user id ran")
    # print(bs_entries)

    user_details = []
    for blood_sugar_obj in bs_entries:
        user_details.append({'bs': blood_sugar_obj.bloodsugar,
                             'date': blood_sugar_obj.input_date.isoformat()})
    # print("this is user details")
    # print(user_details)

    return jsonify({'user_entries': user_details})

if __name__ == "__main__":
    connect_to_db(app)
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)