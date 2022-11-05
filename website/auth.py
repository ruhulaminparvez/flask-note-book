from flask import Blueprint,render_template,request,redirect,flash, url_for
from .models import User ,Note
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

# auth.route("hello")

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email'] #way 1
        password = request.form.get("password") #way 2

        user = User.query.filter_by(email=email).first()
        if user :
            if check_password_hash(user.password,password):
                flash('Logged in successfully',category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password,please try again.",category="error")
        else:
            flash("User doesn\'t exist",category="error")

    return render_template("login.html",user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

@auth.route("/sign-up",methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        email = request.form['email']
        first_name = request.form['name']
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exist",category="error")
        else:
            if len(email) < 4 :
                flash('email must be greater tha 4 characters.' , category="error")
            elif len(first_name) < 3:
                flash('First_name must be greater tha 3 characters.' , category="error")
            elif password != confirm_password:
                flash('Passwords does not match.' , category="error")
            elif len(password) < 7:
                flash('Password Must be at 7 characters.' , category="error")
            else :
                # add user to db
                new_user = User(email=email,first_name=first_name,password=generate_password_hash(password,method="sha256"))
                db.session.add(new_user)
                db.session.commit()
                # login_user(user, remember=True)
                flash('Account created',category='success')
                return redirect(url_for("views.home"))

            
    return render_template("signup.html",user=current_user)