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
from werkzeug.security import check_password_hash


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
def login():
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
        new = Account(username = form.username.data, lastName = form.lastName.data, firstName = form.firstName.data, email = form.email.data, password = generate_password_hash(form.password.data))
        db.session.add(new)
        db.session.commit()
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


@app.route("/enterUsername")
def enterUsername() :
    """
    Allows the players who don't have an account to 
    """
    return render_template("game/username.html")


@app.route("/loadGame")
def loadGame() :
    """
    Simple function that will display a loading page for a few minutes.
    """
    return render_template("game/loading.html")


@app.route("/explainGame")
def explainGame() :
    """
    Function that will return the template that explains people the rules of the game.
    """
    return render_template("game/explainGame.html")


@app.route("/createGame", methods =["GET", "POST"])
@login_required
def createGame():
    """
    Creation of a new game.
    Will ask : - a name
               - a number of themes
               - a number of questions/difficulties
    PS : for the moment, the URL and the creator are hardcoded.
    """
    
    if not current_user.is_authenticated :
        return redirect(url_for("login"))
    
    form = PartieForm()
    if form.validate_on_submit():
        newGame = Game(gameName = form.gameName.data, nbThemes = form.nbThemes.data, nbQuestions = form.nbQuestions.data, URL = "azerty", creator = "Marie Carbonnelle")
        db.session.add(newGame)
        db.session.commit()
        return redirect(url_for('createThemes'))
    return render_template('teacher/createGame.html', form = form)


@app.route("/createThemes", methods =["GET", "POST"])
@login_required
def createThemes() :
    """
    Creation of the different themes.
    Only ask for the name of the theme.
    """
    if not current_user.is_authenticated :
        return redirect(url_for("login"))
    
    form = ThemeForm()
    if form.validate_on_submit():
        newTheme = Theme(themeName = form.themeName.data, associatedGame = "forLater")
        db.session.add(newTheme)
        db.session.commit()
        return redirect(url_for('createQuestions'))
    return render_template('teacher/createThemes.html', form = form)


@app.route("/createQuestions", methods=["GET", "POST"])
@login_required
def createQuestions() :
    """
    Creation of the questions.
    Will ask : - a question
               - 4 different possible answers
               - the correct answer
    """
    if not current_user.is_authenticated :
        return redirect(url_for("login"))
    
    form = QuestionForm()
    if form.validate_on_submit():
        newQuestion = Question(enonce = form.enonce.data, reponseA = form.reponseA.data, reponseB = form.reponseB.data, reponseC = form.reponseC.data, reponseD = form.reponseD.data, bonneReponse = form.bonneReponse.data, difficultyLevel = 3, nbPoints = 3, associatedTheme = "theme")
        db.session.add(newQuestion)
        db.session.commit()
        return redirect(url_for('gameIsCreated'))
    return render_template('teacher/createQuestions.html', form = form)


@app.route("/gameIsCreated")
@login_required
def gameIsCreated() :
    """
    Create the game and shows the url to share for that game.
    """
    return render_template('teacher/gameIsCreated.html')


@app.route("/accessGame")
@login_required
def accessGame() :
    """
    This function allows an user with an account to access
    all the games he created before in order to see them, delete them, modify them, etc ...
    """
    if not current_user.is_authenticated :
        return redirect(url_for("login"))
    return render_template('teacher/accessGame.html')


@app.route("/editGame")
@login_required
def editGame() :
    """
    Allows an user who has an account and has created games to edit them.
    """
    return render_template('teacher/editGame.html')


@app.route("/startSynchro")
@login_required
def startSynchro() :
    """
    Starts the game (synchronous start).
    """
    return render_template('teacher/startSynchro.html')


@app.route("/startAsync")
@login_required
def startAsync() :
    """
    Starts the game (asynchronous start).
    """
    return render_template('teacher/startAsync.html')


@app.route("/deleteGame")
@login_required
def deleteGame() :
    """
    Allows an user to delete his own games.
    """
    return render_template('teacher/deleteGame.html')


@app.route("/accessResults")
@login_required
def accessResults() :
    """
    Shows to the creator of the game the results that have been made previously.
    (Only if there are some).
    """
    return render_template('teacher/accessResults.html')


@app.route("/displayTheme")
def displayTheme() :
    """
    Function that display the themes and ask the player which difficulty he wants.
    """
    return render_template('game/theme.html')


@app.route("/question")
def question() :
    """
    Function that shows the player the question asked and ask him an answer.
    This will be displayed as a QCM.
    """
    return render_template('game/question.html')


@app.route("/correction")
def correction() :
    """
    Will display the correction of the correct answer.
    The player will know how much points he earns.
    """
    return render_template('game/correction.html')


@app.route("/podium")
def podium() :
    """
    Display of a temporary podium between the players.
    """
    return render_template('game/podium.html')


@app.route("/teacherScreen")
def teacherScreen() :
    """
    Display of what a teacher can say :
        - make a new game
        - view their games
        - editing them
        - delete them
        -...
    """
    return render_template('teacher/teacherScreen.html')