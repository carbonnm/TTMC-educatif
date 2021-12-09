from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import IntegerField
from wtforms import SelectField

from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

from application.models import User

class RegisterForm(FlaskForm) :
    """
    This class will be the formulary that the user will have to submit when registering.
    """
    firstName = StringField('Prenom', validators = [InputRequired(message = "Entrez votre prenom"), Length(min = 2, message = "Votre prenom doit faire 2 lettres minimum")])
    lastName = StringField('Nom', validators = [InputRequired(message = "Entrez votre nom"), Length(min = 2, message = "Votre nom doit faire 2 lettres minimum")])
    email = StringField('Email', validators = [InputRequired(message = "Entrez votre email"), Length(min = 7, message = "Votre email doit faire au moins 7 lettres")])
    username = StringField('Pseudo', validators = [InputRequired(message = "Entrez le pseudo que vous desirez"), Length(min = 2, message = "Votre pseudo doit faire minimum 2 caracteres")])
    password = PasswordField('Mot de passe', validators = [InputRequired(message = "Entrez un mot de passe"), Length(min = 5, message = "Votre mot de passe doit faire minimum 5 caracteres")])
    confirmPassword = PasswordField('Confirmation mot de passe', validators = [InputRequired(message = "Veuillez confirmer votre mot de passe"), Length(min = 5), EqualTo('password', message = "Huh, ceci n'etait pas votre mot de passe..")])

    submit = SubmitField('Register')

    def validateUsername(self, field) :
        """
        Function that check if the username is available.
        Exeption :
        -----------
        Raise a validation error if the username is already token.
        """
        if field.data in [x.username for x in User.query.all()] :
            raise ValidationError('Ce pseudo est deja pris')

class LoginForm(FlaskForm) :
    """
    Formulary that needs to be submitted when the user wants to login.
    """
    username = StringField('Pseudo', validators = [InputRequired(message = "Entrez votre pseudo")])
    password = PasswordField('Mot de passe', validators = [InputRequired(message = "Entrez votre mot de passe")])

    submit = SubmitField('Login')

    def validateUsername(self, field):
        """
        Function that check if the username given exists in the db.
        Exeption : 
        -----------
        Raise a validation error if the given username does not exist at all.
        """
        if field.data not in [x.username for x in User.query.all()] :
            raise ValidationError('Votre pseudo n existe pas')

class PartieForm(FlaskForm) :
    """
    Formulary that will be submitted when someone wants to create a game.
    """
    gameName = StringField('Nom de partie', validators = [InputRequired(message = "Entrez un nom pour votre partie"), Length(min = 2, message = "Le nom de votre partie doit faire au moins deux caracteres")])
    nbThemes = IntegerField('Nombre de themes', validators = [InputRequired(message = "Entrez le nombre de themes de votre partie")])
    nbQuestions = IntegerField('Nombre de difficultes', validators = [InputRequired(message = "Entrez le nombre de difficultes par theme, soit le nombre de questions")])

    submit = SubmitField('Enregistrer')