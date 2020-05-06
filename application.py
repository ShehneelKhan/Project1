import os
import re
from datetime import date
import requests
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
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
engine = create_engine("postgres://njpclqortbfebd:8f23a1bc0c6579e17b1cbd74a32565efcff328eeeccd80c4ae76604bb805e7be@ec2-34-200-72-77.compute-1.amazonaws.com:5432/dbugc5i5mcp5rs")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message = "Page Not Found! (404)")


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
        session.pop("user_id",None)
        email_id = request.form.get("email_id")
        pass1 = request.form.get("pass1")
        checking = db.execute("SELECT * FROM users WHERE email = :email",{"email":email_id}).fetchone()
        database_pass = db.execute("SELECT * FROM users WHERE password = :password",{"password":pass1}).fetchone()


        if checking is None:
            return render_template("error.html", message = "This account does not exist!")

        try:
            if pass1 == database_pass[2]:

                session["user_id"]=checking[0]
                session["user_name"]=checking[1]
                session["password"]=checking[2]

                return redirect(url_for("search"),code=307)

        except Exception as e:
            return render_template("error.html", message = "Incorrect Password!")


    return render_template("login.html")



@app.route("/search",methods=["GET","POST"])
def search():
    table = False
    try:


        if session["user_id"] is not None:
            pass


        if session.get("books") is None:
            session["books"] = []

        if request.method == "POST":

            regex = re.compile('[@_#$%^&*!()<>?/\|}{~:]')
            search_book = request.form.get("search_book")


            if search_book == "":
                return render_template("error.html", message = "No such book.")


            if not regex.search(str(search_book)) == None:
                return render_template("error.html", message = "No such book.")



            res = db.execute(" SELECT * FROM books WHERE title LIKE '%"+str(search_book)+"%' OR author LIKE '%"+str(search_book)+"%' OR year LIKE '%"+str(search_book)+"%' OR isbn LIKE '%"+str(search_book)+"%' ;").fetchall()


            for i in res:
                session["books"].append(i)
                table = True



            return render_template("search.html",result=res,table=table)


        return render_template("search.html",user_id = session["user_id"],user_name = session["user_name"],password = session["password"])

    except Exception as e:
        return render_template("error.html", message = "Login First!")


@app.route("/search/<string:isbn>",methods = ["GET","POST"])
def book_details(isbn):

    today = date.today()
    today = today.strftime("%d-%m-%Y")

    try:
        if session["user_id"] is not None:
            pass


        session["comments"] = []

        apiCall = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "PlM0Yn7UcJQxgM6X2k1rA", "isbns": isbn })
        if apiCall.status_code != 200:
            return render_template("error.html", message = "Data is not available for this book")

        apidata = apiCall.json()
        dbdata = db.execute(" SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
        review_check = db.execute("SELECT * FROM reviews WHERE isbn =:isbn AND username =:username",{"isbn":isbn,"username":session["user_name"]}).fetchone()

        if request.method == "POST" and  review_check==None:

            comment = request.form.get("comment")
            rate = request.form.get("rate")

            session["comments"].append(comment)
            db.execute("INSERT INTO reviews (username,isbn,review,rating) VALUES (:username,:isbn,:review,:rating)",{"username":session["user_name"],"isbn":isbn,"review":comment,"rating":rate})
            db.commit()

        elif request.method == "POST" and review_check!=None:
            return render_template("error.html", message = "Only one review per book is allowed!")


        reviews = db.execute("SELECT * FROM reviews WHERE isbn=:isbn",{"isbn":isbn}).fetchall()


    except Exception as e:
        return render_template("error.html", message = "Login First!")

    return render_template("book_details.html", apidata = apidata, dbdata = dbdata , reviews = reviews, today = today)

@app.route("/api/<string:isbn>")
def api(isbn):

    try:
        dbdata = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
        if dbdata is None:
            return jsonify({"Error":"Invalid ISBN!"}),404

        apiCall = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "TzAs9qZiNLUZ3xl1cpDzSg", "isbns": isbn})
        apidata = apiCall.json()

        return jsonify({

                "title":dbdata.title,
                "author":dbdata.author,
                "year":dbdata.year,
                "isbn":dbdata.isbn,
                "review_count":apidata['books'][0]['work_reviews_count'],
                "average_score":apidata['books'][0]['average_rating'],
                      })

    except Exception as e:
        return render_template("error.html", message = "Data is not available for this book")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
