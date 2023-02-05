from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db, Bloodsugar
import crud
from jinja2 import StrictUndefined
from datetime import date, timedelta, datetime
from random import choice

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

inspirational_quotes = [""]

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
    user_email = session.get("email")
    user = crud.get_user_by_email(user_email)
    bs_entries = crud.get_bs_by_user_id(user.user_id)
    insulin_entries = crud.get_Insulin_by_user_id(user.user_id)
    # print("This is bs entry")
    # print(bs_entries)

    return render_template("data.html", bs_entries=bs_entries, insulin_entries=insulin_entries)
    
@app.route("/dataOneButton")
def data_by_first_date():
    """data for data one day button"""

    # get bloodsugar entries in the last day
    oneDayAgo = datetime.now() - timedelta(days=1)
    one = crud.get_bs_by_dates(oneDayAgo)

    total = 0
    length = 0

    for blood_sugar in one:
        total = blood_sugar.bloodsugar + total
        length += 1

    # print("Checking if query works for one")
    # print(total)
    # print(length)
    average = round(total / length)
    # print(average)

    return jsonify({'average': average})

@app.route("/dataTwoButton")
def data_by_two_days():
    # #get bloodsugar entries in the last two days

    twoDaysAgo = datetime.now() - timedelta(days=2)
    two = crud.get_bs_by_dates(twoDaysAgo)

    total = 0
    length = 0

    for blood_sugar in two:
        total = blood_sugar.bloodsugar + total
        length += 1

    # print("Checking if query works for two")
    # print(total)
    # print(length)
    average = round(total / length)

    return jsonify({'average': average})

@app.route("/dataSevenButton")
def data_by_seven_days():
    #get bloodsugar entries in the last seven days

    sevenDaysAgo = datetime.now() - timedelta(days=7)
    seven = crud.get_bs_by_dates(sevenDaysAgo)

    total = 0
    length = 0

    for blood_sugar in seven:
        total = blood_sugar.bloodsugar + total
        length += 1

    # print("Checking if query works for seven")
    # print(total)
    # print(length)
    average = round(total / length)

    return jsonify({'average': average})

@app.route("/dataFourteenButton")
def data_by_fourteen_days():
    #get bloodsugar entries in the last fourteen days

    fourteenDaysAgo = datetime.now() - timedelta(days=14)
    fourteen = crud.get_bs_by_dates(fourteenDaysAgo)

    total = 0
    length = 0

    for blood_sugar in fourteen:
        total = blood_sugar.bloodsugar + total
        length += 1

    # print("Checking if query works for fourteen")
    # print(total)
    # print(length)
    average = round(total / length)

    return jsonify({'average': average})

@app.route("/dataThirtyButton")
def data_by_thirty_days():
    #get bloodsugar entries in the last thirty days

    thirtyDaysAgo = datetime.now() - timedelta(days=30)
    thirty = crud.get_bs_by_dates(thirtyDaysAgo)

    total = 0
    length = 0

    for blood_sugar in thirty:
        total = blood_sugar.bloodsugar + total
        length += 1

    # print("Checking if query works for thirty")
    # print(total)
    # print(length)
    average = round(total / length)

    return jsonify({'average': average})

@app.route("/dataSixtyButton")
def data_by_sixty_days():
    #get bloodsugar entries in the last sixty days

    sixtyDaysAgo = datetime.now() - timedelta(days=60)
    sixty = crud.get_bs_by_dates(sixtyDaysAgo)

    total = 0
    length = 0

    for blood_sugar in sixty:
        total = blood_sugar.bloodsugar + total
        length += 1

    # print("Checking if query works for sixty")
    # print(total)
    # print(length)
    average = round(total / length)

    return jsonify({'average': average})
    
@app.route("/dataNinetyButton")
def data_by_ninety_days():
    #get bloodsugar entries in the last ninety days

    ninetyDaysAgo = datetime.now() - timedelta(days=90)
    ninety = crud.get_bs_by_dates(ninetyDaysAgo)

    total = 0
    length = 0

    for blood_sugar in ninety:
        total = blood_sugar.bloodsugar + total
        length += 1

    # print("Checking if query works for ninety")
    # print(total)
    # print(length)
    average = round(total / length)

    return jsonify({'average': average})


@app.route("/entries")
def get_entries():
    """getting bloodsugar entries for chart"""

    """get user in session details, then get entries on corresponding user based on user_id."""
    user_email = session.get('email')
    user = crud.get_user_by_email(user_email)
    # print("get user by email ran")
    # print(user)
    bs_entries = crud.get_bs_by_user_id(user.user_id)
    # print("get bs by user id ran")
    # print(bs_entries)

    """looping through bs_entries and getting each object. 
    Then we append the bs number and its date as key valued pairs to user_details"""
    user_details = []
    for blood_sugar_obj in bs_entries:
        user_details.append({'bs': blood_sugar_obj.bloodsugar,
                             'date': blood_sugar_obj.input_date.isoformat()})
    # print("this is user details")
    # print(user_details)

    """jsonify user_details to send to chart."""
    return jsonify({'user_entries': user_details})

if __name__ == "__main__":
    connect_to_db(app)
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)