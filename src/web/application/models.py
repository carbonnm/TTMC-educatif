from flask_login import UserMixin
from application import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from application import login_manager

class Player() :
    """
    Player class
    ---------------
    This class is made for people that will not have an account.
    They still needs to be identified with a username.
    """
    __tablename__ = 'player'
    IDPlayer = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Colum(db.String(255), nullable = False)
    #Maybe a link with an account here ?

    def getUsername(self) :
        """
        Getter of the username.
        Return : 
        ----------
        Username
        """
        return self.username


class Account(UserMixin, db.Model) :
    """
    Account class
    --------------
    This class will contain all the informations about the users who have an account.
    """
    #Initialisation
    __tablename__ = 'account'

    #DB
    IDAccount = db.Column(db.Integer, primary_key = True, autoincrement = True)
    firstName = db.Column(db.String(255), nullable = False)
    lastName = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False, unique = True)
    username = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)

    def getUsername(self) :
        """
        Getter of the username.
        Return : 
        ----------
        Username
        """
        return self.username

    def setPassword(self, password) :
        """
        Setter of the password in the database.
        We use for that the function generate_password_hash so that the password is crypted in the database. 
        """
        self.password = generate_password_hash(password)
    
    def checkPassword(self, password) :
        """
        Check if the password do correspond.
        Return :
        ----------
        True if the passwords do correspond, False otherwise.
        """
        return check_password_hash(self.password, password)

    def __repr__(self) :
        """
        How users will be represented.
        Return :
        ----------
        Representation of an user.
        """
        return "<User id : %d, username : %s, lastName : %s, firstName : %s, email : %s>" %(self.IDAccount, self.username, self.lastName, self.firstName, self.email)
        

#Games class
class Game() :
    """
    Game class
    ---------------
    This class will contain all the informations related to a specific game.
    ie : its name, the number of themes, the number of questions.
    """
    __tablename__ = 'game'

    IDGame = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    nbThemes = db.Column(db.Integer, nullable = False)
    nbQuestions = db.Column(db.Integer, nullable = False)
    URL = db.Column(db.String(255), nullable = False)
    #Necessity to make a link here
    creator = db.Column(db.String(255), nullable = False)
    
    def getName(self) :
        """
        Getter of the name of the game.
        Return :
        ---------
        The name of the game.
        """
        return self.name


class Theme() :
    """
    Theme class
    -------------
    Class that countains informations related to the themes, that are linked to a specific game.
    """
    IDTheme = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nameTheme = db.Column(db.String(255), nullable = False)
    #Necessity to make a link here ! 
    associatedGame = db.Column(db.String(255), nullable = False)


class Question() :
    """
    Question class
    -----------------
    Class that countains informations related to the questions, linked to a specific theme
    (and therefore a specific game too).
    """
    IDQuestion = db.Column(db.Integer, primary_key = True, autoincrement = True)
    enonce = db.Column(db.String(255), nullable = False)
    reponseA = db.Column(db.String(255), nullable = False)
    reponseB = db.Column(db.String(255), nullable = False)
    reponseC = db.Column(db.String(255), nullable = False)
    reponseD = db.Column(db.String(255), nullable = False)
    bonneReponse = db.Column(db.String(255), nullable = False)
    difficultyLevel = db.Column(db.Integer, nullable = False)
    nbPoints = db.Column(db.Integer, nullable = False)
    #Neccessity to make a link here !!!
    associatedTheme = db.Column(db.String(255), nullable = False)


class Session() :
    """
    Session class
    ---------------
    Class that concerns a certain session of a given game.
    This is explained by the fact that a game can be played multiple times.
    That's why we used different sessions, even tho they can concern the same game somtimes.
    """
    IDSession = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #Necessity to make a link here
    gameAssociated = db.Column(db.String(255), nullable = False)
    status = db.Column(db.String(255), nullable = False)


class Answer() :
    """
    Answer class
    ---------------
    Class that concerns the answers given by a certain player to a certain question.
    """
    IDAnswer = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #Necessity to make a link here !!!
    usernameAssociated = db.Column(db.String(255), nullable = False)
    #Necessity to make a link here !!!
    enonce = db.Column(db.String(255), nullable = False)
    answerGiven = db.Column(db.String(255), nullable = False)
    #Necessity to make a link here !!!
    sessionAssociated = db.Column(db.String(255), nullable = False)


#The DB part :
db.drop_all()
db.create_all()

db.session.commit()

# callback to reload the user object
@login_manager.user_loader
def load_user(userID):
    return Player.query.get(int(userID))