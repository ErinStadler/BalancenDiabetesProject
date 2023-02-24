from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import timedelta, datetime
from random import choice
import json
import hashlib
import pync


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

motivational_quotes = ["“All our dreams can come true, if we have the courage to pursue them” — Walt Disney", "“The secret to getting ahead is getting started.” — Mark Twain", 
                       "“Don’t limit yourself. Many people limit themselves to what they think they can do. You can go as far as your mind lets you. What you believe, remember, you can achieve.” —Mary Kay Ash",
                       "“The best time to plant a tree was 20 years ago. The second best time is now.” ―Chinese Proverb",
                       "“It’s hard to beat a person who never gives up.” —Babe Ruth", "“If people are doubting how far you can go, go so far that you can’t hear them anymore.” —Michele Ruiz",
                       "“We need to accept that we won’t always make the right decisions, that we’ll screw up royally sometimes―understanding that failure is not the opposite of success, it’s part of success.” ―Arianna Huffington",
                       "“You’ve gotta dance like there’s nobody watching, love like you’ll never be hurt, sing like there’s nobody listening, and live like it’s heaven on earth.” —William W. Purkey",
                       "“Fairy tales are more than true: not because they tell us that dragons exist, but because they tell us that dragons can be beaten.”―Neil Gaiman", "“When one door of happiness closes, another opens; but often we look so long at the closed door that we do not see the one which has been opened for us.” ―Helen Keller",
                       "“Do one thing every day that scares you.” ―Eleanor Roosevelt", "“It’s no use going back to yesterday, because I was a different person then.” ―Lewis Carroll",
                       "“Do what you feel in your heart to be right―for you’ll be criticized anyway.” ―Eleanor Roosevelt", "“Happiness is not something ready made. It comes from your own actions.” ―Dalai Lama XIV",
                       "“Whatever you are, be a good one.” ―Abraham Lincoln", "“The same boiling water that softens the potato hardens the egg. It’s what you’re made of. Not the circumstances.” —Unknown", 
                       "“If we have the attitude that it’s going to be a great day it usually is.” —Catherine Pulsifier",
                       "“You can either experience the pain of discipline or the pain of regret. The choice is yours.” —Unknown", "“Impossible is just an opinion.” —Paulo Coelho",
                       "“Your passion is waiting for your courage to catch up.” —Isabelle Lafleche", "“Magic is believing in yourself. If you can make that happen, you can make anything happen.” —Johann Wolfgang Von Goethe", "“If something is important enough, even if the odds are stacked against you, you should still do it.” —Elon Musk",
                       "“Hold the vision, trust the process.” —Unknown", "“Don’t be afraid to give up the good to go for the great.” —John D. Rockefeller", "“People who wonder if the glass is half empty or full miss the point. The glass is refillable.” —Unknown",
                       "“If you hear a voice within you say, ‘You cannot paint,’ then by all means paint, and that voice will be silenced.” ―Vincent Van Gogh", "“How wonderful it is that nobody need wait a single moment before starting to improve the world.” ―Anne Frank",
                       "“Some people want it to happen, some wish it would happen, others make it happen.” ―Michael Jordan", "“Great things are done by a series of small things brought together.” ―Vincent Van Gogh"]

@app.route("/")
def homepage():
    """homepage a use starts at"""

    return render_template('startup.html')

@app.route("/homepage")
def homepageSignedIn():
    """Homepage for users when logged in"""
    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)

    return render_template('homepage.html', name=user.name)

@app.route("/info")
def infoPageSignedIn():
    """info page when user's logged in"""

    return render_template('info.html')

@app.route("/login")
def login_page():
    """takes user to the login page"""

    return render_template("login.html")

@app.route("/account")
def account_page():
    """takes user to account page"""

    return render_template("account.html")

@app.route("/foodTracker")
def food_tracker():
    """takes a user to food tracking page"""
    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)
    food = crud.get_food_by_user_id(user.user_id)

    return render_template("foodTracker.html", food=food)

@app.route("/data")
def data_page():
    """opens data page"""
    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)
    bs_entries = crud.get_bs_by_user_id(user.user_id)
    insulin_entries = crud.get_Insulin_by_user_id(user.user_id)

    return render_template("data.html", bs_entries=bs_entries, insulin_entries=insulin_entries)

@app.route("/logout")
def logout():

    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)
    session.pop(user, None)

    return redirect('/login')

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

    salt = "ftviyogy8osbzyfucesuo"
    database_password = password+salt
    hashed = hashlib.md5(database_password.encode())

    user = crud.get_user_by_email(email)

    if not user or user.password != hashed.hexdigest():
        flash("email or password is incorrect.")

        return redirect("/login")

    else:
        user_name = user.name
        session['email'] = user.email
        flash(f"login successful! Welcome back {user.name}")

    return render_template("homepage.html",
                           name=user_name)

@app.route("/create_food", methods=["POST"])
def create_food():
    """creating a food item for user to find later"""

    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)

    food_name = request.args.get("name")
    serving = request.args.get("serving")
    calories = request.args.get("calories")
    carbs = request.args.get("carbs")

    food = crud.create_food(user.user_id, food_name, serving, calories, carbs)
    db.session.add(food)
    db.session.commit()

    return redirect("/foodTracker") 

@app.route("/add_food", methods=['POST'])
def adding_food():

    foodToAdd = str(request.json.get('foodToAdd'))
    food = crud.get_food_by_name(foodToAdd)
    print("this is food")
    print(food)

    if food == None:
        flash("food not found.")
    
    else:

        return jsonify({"name": food.food_name, "serving": food.serving_size, "calories": food.calories, "carbs": food.carbs})

@app.route("/user", methods=["POST"])
def register():
    """check if the user already exists, and if not, create a 
    new account"""

    email = request.form.get("email")
    password = request.form.get("password")
    min_range = request.form.get("min_range")
    max_range = request.form.get("max_range")
    name = request.form.get("name")

    salt = "ftviyogy8osbzyfucesuo"
    database_password = password+salt
    hashed = hashlib.md5(database_password.encode())

    if crud.get_user_by_email(email):
        """if a user exists, tell them and redirect back to sign up page 
        (they can decide to go to login then if they want)"""
        flash("user already exists")

        return redirect("/signup")

    else:
        """if no user with email already exists, then create user."""
        
        if min_range or max_range == '':

            user = crud.create_user_with_defaults(email, hashed.hexdigest(), name)
            db.session.add(user)
            db.session.commit()
            flash("account successfully created! Please login.")

            return redirect("/login")

        else:
            user = crud.create_user(email, hashed.hexdigest(), min_range, max_range, name)

            db.session.add(user)
            db.session.commit()
            flash("account successfully created! Please login.")

            return redirect("/login")
        
@app.route("/update_min_range", methods=['POST'])
def update_min_range():
    """updates the users min_range"""

    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)

    new_min = request.form.get('update_min_range')

    if int(user.min_range) != int(new_min):

        crud.update_min(new_min, user.user_id)

        flash(f"Min Range Updated! It is now {new_min}.")

    else:
        flash(f"your min range is already {new_min}, please enter another value to update min range.")

    return redirect("/account")

@app.route("/update_max_range", methods=['POST'])
def update_max_range():
    """updates the users max_range"""

    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)

    new_min = request.form.get('update_max_range')

    if int(user.max_range) != int(new_min):

        crud.update_max(new_min, user.user_id)

        flash(f"Min Range Updated! It is now {new_min}.")

    else:
        flash(f"your min range is already {new_min}, please enter another value to update min range.")

    return redirect("/account")

@app.route("/update_name", methods=['POST'])
def update_name():
    """updates the users name"""

    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)

    new_name = request.form.get('update_name')

    if user.name != new_name:

        crud.update_name(new_name, user.user_id)

        flash(f"You're name has been Updated!")

    else:
        flash(f"{new_name}, is already set as your name.")

    return redirect("/account")

@app.route("/update_password", methods=['POST'])
def update_password():
    """updates the users password"""
    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)

    new_pass = request.form.get('update_password')

    salt = "ftviyogy8osbzyfucesuo"
    database_password = new_pass+salt
    hashed = hashlib.md5(database_password.encode())

    if user.password != new_pass:

        crud.update_password(hashed.hexdigest(), user.user_id)

        flash(f"You're password has been Updated!")

    else:
        flash(f"This is already set as your password.")

    return redirect("/account")
        
@app.route("/create_bs_entry", methods=["POST"])
def create_bs_entry():
    """creates a blood sugar entry if correct value entered"""
    
    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)
    bs_entry = request.form.get("bloodsugar_entry")
    current_date = datetime.now()

    user_name = user.name

    min = int(user.min_range)
    # print("this is the min")
    # print(min)
    max = int(user.max_range)
    # print("this is the max")
    # print(max)

    """check if a value was given. If no, then flash message to put in number.
    If yes, then add the blood sugar to table"""
    if bs_entry == '':
        flash('Please enter a value for blood sugar to create entry.')

    else:
        """Checking now if blood sugar is below, above or between the min and max range. Api quotes to be implemented here soon"""

        if int(bs_entry) > max:
            entry = crud.create_bloodsugar(user.user_id, int(bs_entry), current_date)
            flash(choice(motivational_quotes))

            db.session.add(entry)
            db.session.commit()

        elif int(bs_entry) < min:
            entry = crud.create_bloodsugar(user.user_id, int(bs_entry), current_date)
            flash("You're bloodsugar is low. Please eat some carbs, if needed.")

            db.session.add(entry)
            db.session.commit()

        else:
            entry = crud.create_bloodsugar(user.user_id, int(bs_entry), current_date)
            flash(choice(motivational_quotes))

            db.session.add(entry)
            db.session.commit()

    return render_template("homepage.html",
                           name=user_name)

@app.route("/create_insulin_entry", methods=["POST"])
def create_insulin_entry():
    """creates an insulin entry when user inputs correct value"""
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
    
@app.route(f"/blood_sugars_days_back", methods=['POST'])
def data_by_days():
    """get bloodsugar averages of how ever many days the user chooses."""
    user_email = session.get('email')
    user = crud.get_user_by_email(user_email)
    daysBack = int(request.json.get('daysBack'))

    daysAgo = datetime.now() - timedelta(days=daysBack)
    data = crud.get_bs_by_dates(user.user_id, daysAgo)

    total = 0
    length = 0

    for blood_sugar in data:
        total = blood_sugar.bloodsugar + total
        length += 1

    average = round(total / length)

    return jsonify({'average': average})

@app.route("/entries")
def get_entries():
    """getting bloodsugar entries for chart"""
    user_email = session.get('email')
    user = crud.get_user_by_email(user_email)
    
    data = crud.get_bs_by_user_id(user.user_id)

    bs_data = []

    for blood_sugar_obj in data:
        bs_data.append({'bs': blood_sugar_obj.bloodsugar,
                             'date': blood_sugar_obj.input_date.isoformat()})

    return jsonify({'bs_data': bs_data})

if __name__ == "__main__":
    connect_to_db(app)
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)