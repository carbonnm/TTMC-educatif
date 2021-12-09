import re
from application import app

from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

from application.forms import *

from application.models import User
from application.models import users

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.route("/")
def main():
    if current_user.is_authenticated :
        return render_template()
    else :
        return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login() :
    if current_user.is_authenticated :
        return redirect(url_for('main'))
    
    form = LoginForm()
    #Verification of the form
    if form.validate_on_submit():
        #Let's "init" the user
        user = next((x for x in users if form.username == x.getUsername() and form.password == x.getPassword()), None)
        if user is not None :
            login_user(user)
            return redirect(url_for('main'))
        #Password or username might be wrong
        else :
            return redirect(url_for('login'))
    else :
        return render_template('login.html',form = form)

@app.route("/register", methods=["GET", "POST"])
def register() :
    if current_user.is_authenticated :
        #User is logged
        return redirect(url_for("main"))
    
    form = RegisterForm()
    if form.validate_on_submit():
        #Add the user
        new = User(form.firstName.data, form.lastName.data, form.email.data, form.password.data)
        users.append(new)
        return redirect(url_for("login"))

    else : 
        return render_template('registration.html', form = form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated :
        logout_user()
    return redirect(url_for("main"))

@app.route("/admin")
def admin() :
    if current_user.role == "admin" :
        return render_template("admin.html", users = users)
    else :
        #He's not an admin
        return redirect(url_for("main"))

@app.route("/createGame", methods =["GET", "POST"])
def createGame():
    if not current_user.is_authenticated :
        return redirect(url_for("login"))
    
    form = PartieForm()
    #if form.validate_on_submit() :