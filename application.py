import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://srcsvtqzajbsqa:2816e69dcd518b6d8c414d3104dc153014046967147714f3d525fa2b2ed783ca@ec2-54-86-170-8.compute-1.amazonaws.com:5432/d1f5f7l7rlidba")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method =="POST":
        min_chars = 7
        email_id=request.form.get("email_id")
        pass1 = request.form.get("pass1")
        pass2 = request.form.get("pass2")
        if email_id == "" or pass1 == "" or pass2 == "":
            return render_template("error.html", message="You cant leave a field empty!")

        elif pass1 != pass2:
            return render_template("error.html", message="Your password does not match!")

        if len(pass1) < min_chars:
            return render_template("error.html", message="Your password should be atleast {} characters long!".format(min_chars))

        else:
            db.execute("INSERT INTO users (email,password) VALUES (:email,:password)",{"email":email_id,"password":pass1})
            db.commit()
            return render_template("login.html")



    else:
        return render_template("register.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email_id = request.form.get("email_id")
        pass1 = request.form.get("pass1")
        checking = db.execute("SELECT email FROM users WHERE email = :email",{"email":email_id}).fetchone()
        database_pass = db.execute("SELECT * FROM users WHERE password = :password",{"password":pass1}).fetchone()

        if checking is None:
            return render_template("error.html", message = "This account does not exist!")

        try:
            if pass1 == database_pass[2]:
                return render_template("index.html")

        except Exception as e:
            return render_template("error.html", message = "Incorrect Password!")


    return render_template("login.html")
