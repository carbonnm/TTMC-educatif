from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

#Users class 
class User(UserMixin, db.Model) :
    """User class :
    This class will contain all the informations about the users in the database.
    """
    #Initialisation
    __tablename__ = 'users'

    #DB
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String(255), nullable = False, unique = True)
    lastName = db.Column(db.String(255), nullable = False)
    firstName = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False)
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
        return "<User id : %d, username : %s, lastName : %s, firstName : %s, email : %s>" %(self.id, self.username, self.lastName, self.firstName, self.email)
        

#Games class
class Game() :
    """
    This class will contain all the informations related to a specific game.
    ie : its name, the number of themes, the number of questions.
    """
    __tablename__ = 'games'

    #db
    id = db.Colum(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    nbThemes = db.Column(db.Integer, nullable = False)
    dbQuestions = db.Column(db.Integer, nullable = False)
    
    def getName(self) :
        """
        Getter of the name of the game.
        Return :
        ---------
        The name of the game.
        """
        return self.name