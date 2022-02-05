"""
This part of the code countains all the formularies of my game.
This means : 
- Entering of a pseudo to play (This is explained by the fact that people don't HAVE TO have an account to play
                                but we ask at least an username)
- Registration Formulary (to have an account)
- Login Formulary
- Modification of a profile Formulary
- Modification of the password Formulary
- Creation of a new game Formulary
- Modification of a game Formulary
- Creation des differents themes de la partie
- Creation des differentes questions de la partie
"""
from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import IntegerField

from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired

from application.models import *

class usernameForm(FlaskForm) :
    """
    Username Form
    -----------------
    Formulary used to save the username of the person that plays
    if she doesn't have an account.
    """
    username = StringField('Pseudo', validators = [InputRequired(message = "Entrez le pseudo que vous desirez"), Length(min = 2, message = "Votre pseudo doit faire minimum 2 caracteres")])

    submit = SubmitField('Valider')

    def validateUsername(self, field) :
        """
        Function that check if the username is available.
        Exeption :
        -----------
        Raise a validation error if the username is already token.
        """
        if field.data in [x.username for x in Player.query.all()] :
            raise ValidationError('Ce pseudo est deja pris')
        

class RegisterForm(FlaskForm) :
    """
    Register Form
    ----------------
    Formulary that the user will have to submit when registering.
    """
    firstName = StringField('Prenom', validators = [InputRequired(message = "Entrez votre prenom"), Length(min = 2, message = "Votre prenom doit faire 2 lettres minimum")])
    lastName = StringField('Nom', validators = [InputRequired(message = "Entrez votre nom"), Length(min = 2, message = "Votre nom doit faire 2 lettres minimum")])
    email = StringField('Email', validators = [InputRequired(message = "Entrez votre email"), Length(min = 7, message = "Votre email doit faire au moins 7 lettres")])
    username = StringField('Pseudo', validators = [InputRequired(message = "Entrez le pseudo que vous desirez"), Length(min = 2, message = "Votre pseudo doit faire minimum 2 caracteres")])
    password = PasswordField('Mot de passe', validators = [InputRequired(message = "Entrez un mot de passe"), Length(min = 5, message = "Votre mot de passe doit faire minimum 5 caracteres")])
    confirmPassword = PasswordField('Confirmation mot de passe', validators = [InputRequired(message = "Veuillez confirmer votre mot de passe"), Length(min = 5), EqualTo('password', message = "Huh, ceci n'etait pas votre mot de passe..")])

    submit = SubmitField('Creer mon compte')

    def validateUsername(self, field) :
        """
        Function that check if the username is available.
        Exeption :
        -----------
        Raise a validation error if the username is already token.
        """
        if field.data in [x.username for x in Player.query.all()] :
            raise ValidationError('Ce pseudo est deja pris')


class LoginForm(FlaskForm) :
    """
    Login Form 
    --------------
    Formulary that needs to be submitted when the user wants to login.
    """
    username = StringField('Pseudo', validators = [InputRequired(message = "Entrez votre pseudo")])
    password = PasswordField('Mot de passe', validators = [InputRequired(message = "Entrez votre mot de passe")])

    submit = SubmitField('Se connecter')

    def validateUsername(self, field):
        """
        Function that check if the username given exists in the db.
        Exeption : 
        -----------
        Raise a validation error if the given username does not exist at all.
        """
        if field.data not in [x.username for x in Player.query.all()] :
            raise ValidationError('Votre pseudo n existe pas')


class UpdateProfileForm(FlaskForm) :
    """
    UpdateProfile Form
    -----------------
    Asks the user different informations about him in order to update his profile.
    """
    firstName = StringField('Prenom', validators = [DataRequired(message = "Entrez votre nouveau prenom ici")])
    lastName = StringField('Nom', validators = [DataRequired(message = "Entrez votre nouveau nom ici")])
    email = StringField('Email', validators = [DataRequired(message = "Entrez votre nouvel email ici")])

    submit = SubmitField('Mettre a jour')


class UpdatePasswordForm(FlaskForm) :
    """
    UpdatePassword Form
    -----------------
    Asks the user different informations about him in order to update his password.
    """
    password = PasswordField('Mot de passe', validators = [DataRequired(message = "Choisissez un nouveau mot de passe."), Length(min = 5, message = "Votre mot de passe doit faire minimum 5 caracteres")])
    confirmPassword = PasswordField('Confirmation du mot de passe', validators = [DataRequired(message = "Confirmez votre mot de passe"), EqualTo('password', message = "Ce n'est pas le mot de passe que vous venez de mettre")])

    submit = SubmitField('Mettre a jour')
    

class PartieForm(FlaskForm) :
    """
    Partie Form
    ---------------
    Formulary that will be submitted when someone wants to create a game.
    """
    gameName = StringField('Nom de partie', validators = [InputRequired(message = "Entrez un nom pour votre partie"), Length(min = 2, message = "Le nom de votre partie doit faire au moins deux caracteres")])
    nbThemes = IntegerField('Nombre de themes', validators = [InputRequired(message = "Entrez le nombre de themes de votre partie")])
    nbQuestions = IntegerField('Nombre de difficultes', validators = [InputRequired(message = "Entrez le nombre de difficultes par theme, soit le nombre de questions")])

    submit = SubmitField('Creer la partie')


class ThemeForm(FlaskForm) :
    """
    Theme Form
    -------------
    Formulary used to define the differents themes associated to a game
    """
    themeName = StringField('Nom du theme', validators = [InputRequired(message = "Entrez le nom d'un theme")])

    submit = SubmitField('Valider le theme')


class QuestionForm(FlaskForm) :
    """
    Question Form
    ----------------
    Formulary used to create the different questions associated to a theme
    """
    enonce = StringField('Enonce de la question', validators = [InputRequired(message = "Entrez l'enonce de la question")])
    reponseA = StringField('Reponse A', validators = [InputRequired(message = "Entrez une premiere possibilite de reponse")])
    reponseB = StringField('Reponse B', validators = [InputRequired(message = "Entrez une deuxieme possibilite de reponse")])
    reponseC = StringField('Reponse C', validators = [InputRequired(message = "Entrez une trosieme possibilite de reponse")])
    reponseD = StringField('Reponse D', validators = [InputRequired(message = "Entrez une quatrieme possibilite de reponse")])
    bonneReponse = StringField('Bonne reponse', validators = [InputRequired(message = "Entrez la bonne reponse")])

    submit = SubmitField('Valider cette question')