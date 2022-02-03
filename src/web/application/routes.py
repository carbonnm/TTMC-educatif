from application import app

from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash

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
    Return :
    ---------
    Redirection to the error html page.
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """
    Handler of the errors.
    Return :
    ---------
    Redirection to the error html page.
    """
    return render_template('500.html'), 500

@app.route("/")
def main():
    """
    Main page.
    Return :
    ---------
    Redirection to the home page
    """
    return render_template('base.html')

@app.route("/login", methods=["GET", "POST"])
def login() :
    """
    Login function.
    Return :
    ---------
    Redirection to the login page.
    """
    if current_user.is_authenticated :
        flash("Vous êtes déjà connecté à votre compte")
        return redirect(url_for('main'))
    
    form = LoginForm()
    #Verification of the form
    if form.validate_on_submit():
        #Let's "init" the user
        user = User.query.filter_by(username = form.username.data).first()
        #Verification of the user password.
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main'))
        #Password or username might be wrong
        else :
            flash("Votre mot de passe ou votre pseudo est incorrect")
            return redirect(url_for('login'))
    else :
        return render_template('login.html',form = form)

@app.route("/register", methods=["GET", "POST"])
def register() :
    """
    Registration function. If the user is already logged, then we'll go back to the home page.
    Return :
    ---------
    Redirection to the registration page.
    Once the registration is done, redirection to the login page.
    """
    if current_user.is_authenticated :
        #User is logged
        flash("Vous êtes déjà connecté à votre compte.")
        return redirect(url_for("main"))
    
    form = RegisterForm()
    if form.validate_on_submit():
        #Add the user
        new = User(username = form.username.data, firstName = form.firstName.data, lastName = form.lastName.data, email = form.email.data, password = generate_password_hash(form.password.data))
        db.session.add(new)
        db.session.commit()
        return redirect(url_for("login"))

    else : 
        return render_template('registration.html', form = form)


@app.route("/logout")
def logout():
    """
    Logout of the user. The user will go back to the home page. 
    Return :
    ---------
    Redirection to the main page.
    """
    if current_user.is_authenticated :
        logout_user()
    return redirect(url_for("main"))


@app.route("/profile")
@login_required
def profile() :
    """
    This will show the informations about the user's profile.
    Return :
    ----------
    Redirection to the profile page.
    """
    if current_user.is_authenticated :
        return render_template('profile.html')

@app.route("/editProfile/<int:id>")
@login_required
def editProfile(id) :
    """
    This will allow the user to edit his profile's information.
    """
    user = User.query.filter_by(id = id).first()
    if user is None :
        flash("Cet utlisateur n'existe pas")
        return redirect(url_for('main'))
    form = RegisterForm()
    if request.method == 'POST':
        user.username = form.username.data
        user.lastName = form.lastName.data
        user.firstName = form.firstName.data
        user.email = form.email.data

        db.session.commit()
        return redirect(url_for('main'))

    else :
        form.username.data = user.username
        form.lastName.data = user.lastName
        form.firstName.data = user.firstName
        form.email.data = user.email

        return render_template('editProfile.html', form = form, id = id)


@app.route("/createGame", methods =["GET", "POST"])
def createGame():
    if not current_user.is_authenticated :
        return redirect(url_for("login"))
    
    form = PartieForm()
    #if form.validate_on_submit() :

@app.route("/game")
def game():
    return render_template('game.html')