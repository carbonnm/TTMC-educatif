from application import app
from application import db

from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import jsonify

from werkzeug.exceptions import abort

from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

from application.forms import *
from application.models import *


@app.errorhandler(404)
def page_not_found(e):
    """
    Handler of the errors.
    Display 404.html whenever a page is not found
    """
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """
    Handler of the errors.
    Display 500.html whenever a server error occures.
    """
    return render_template('errors/500.html'), 500

@app.route("/")
def homepage():
    """
    Main page.
    Redirection to the home page
    """
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login() :
    """
    Login function.
    Redirection to the login page.
    Exceptions :
    ----------------
    User already connected to his account.
    Username does not exist.
    The password is not correct.
    """
    if current_user.is_authenticated :
        flash("Vous êtes déjà connecté à votre compte", "warning")
        return redirect(url_for('homepage'))
    
    form = LoginForm()
    #Verification of the form
    if form.validate_on_submit():
        #Let's "init" the user
        user = Account.query.filter_by(username = form.username.data).first()
        #Verification of the user password.
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('homepage'))
        #Password or username might be wrong
        else :
            flash("Votre mot de passe ou votre pseudo est incorrect", "warning")
            return redirect(url_for('login'))
    return render_template('account/login.html',form = form)


@app.route("/register", methods=["GET", "POST"])
def register() :
    """
    Registration function. If the user is already logged, then we'll go back to the home page.
    Redirection to the registration page.
    Exception :
    --------------
    User already logged in.
    """
    if current_user.is_authenticated :
        #User is logged
        flash("Vous êtes déjà connecté à votre compte.", "info")
        return redirect(url_for("homepage"))
    
    form = RegisterForm()
    if form.validate_on_submit():
        #Add the user
        new = Account(firstName = form.firstName.data, lastName = form.lastName.data, email = form.email.data, username = form.username.data, password = generate_password_hash(form.password.data))
        db.session.add(new)
        db.session.commit()
        print("youhou")
        login_user(new)
        return redirect(url_for("homepage"))

    return render_template('account/registration.html', form = form)


@app.route("/logout")
def logout():
    """
    Logout of the user. The user will go back to the home page. 
    Redirection to the main page.
    """
    if current_user.is_authenticated :
        logout_user()
    return redirect(url_for("homepage"))


@app.route("/profile")
@login_required
def profile() :
    """
    This will show the informations about the user's profile.
    Redirection to the profile page.
    """
    if current_user.is_authenticated :
        return render_template('profile/profile.html')


@app.route("/deleteProfile")
@login_required
def deleteProfile() :
    """
    Possibility for the user to delete his profile.
    """
    db.session.delete(current_user)
    db.session.commit()
    logout()
    return redirect(url_for("homepage"))


@app.route("/editProfile", methods=["GET", "POST"])
@login_required
def editProfile() :
    """
    This will allow the user to edit his profile's information.
    """
    form = UpdateProfileForm()

    if form.validate_on_submit():
        current_user.lastName = form.lastName.data
        current_user.firstName = form.firstName.data
        current_user.email = form.email.data

        db.session.commit()
        return redirect(url_for('profile'))

    else :
        form.lastName.data = current_user.lastName
        form.firstName.data = current_user.firstName
        form.email.data = current_user.email

        return render_template('profile/editProfile.html', form = form)


@app.route("/editMDP", methods=["GET", "POST"])
@login_required
def editMDP():
    """
    Allows the user to change his password.
    """
    form = UpdatePasswordForm()

    if form.validate_on_submit():
        current_user.set_pwd(form.password.data)
        db.session.commit()
        return redirect(url_for("profile"))
    else:
        return render_template("profile/editMDP.html", form=form)


@app.route("/createGame", methods =["GET", "POST"])
@login_required
def createGame():
    
    if not current_user.is_authenticated :
        return redirect(url_for("login"))
    
    form = PartieForm()
    #if form.validate_on_submit() :


@app.route("/accessGame")
@login_required
def accessGame() :
    """
    This function allows an user with an account to access
    all the games he created before in order to see them, delete them, modify them, etc ...
    """
    if not current_user.is_authenticated :
        return redirect(url_for("login"))


@app.route("/game")
def game():
    return render_template('game.html')