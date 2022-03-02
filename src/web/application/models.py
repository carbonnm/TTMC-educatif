from flask_login import UserMixin
from application import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from application import login_manager


class Account(UserMixin, db.Model) :
    """
    Account class
    --------------
    This class will contain all the information about the users who have an account.
    """
    #Initialisation
    __tablename__ = 'account'

    #DB
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), nullable = False, unique = True)
    lastName = db.Column(db.String(255), nullable = False)
    firstName = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)

    def getUsername(self) :
        """
        Getter of the username.
        Return : 
        ----------
        Username
        """
        return self.id

    def setPassword(self, password) :
        """
        Setter of the password in the database.
        We use for that the function generate_password_hash so that the password is cripted in the database.
        """
        self.password = generate_password_hash(password)
        db.session.commit()
    
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
        Representation of a user.
        """
        return "<User id : %d, username : %s, lastName : %s, firstName : %s, email : %s>" % (self.id, self.username, self.lastName, self.firstName, self.email)
    

    
class Player(db.Model) :
    """
    Player class
    ---------------
    This class is made for people that will not have an account.
    They still need to be identified with a username.
    """
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), nullable = False)
    #Maybe a link with an account here ?

    def getUsername(self) :
        """
        Getter of the username.
        Return : 
        ----------
        Username
        """
        return self.username

    def __repr__(self) :
        """
        Representation of a player.
        """
        return "<Player id : %d, username : %s>" % (self.id, self.username)


#Games class
class Game(db.Model) :
    """
    Game class
    ---------------
    This class will contain all the information related to a specific game.
    ie : its name, the number of themes, the number of questions.
    """
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    gameName = db.Column(db.String(255), nullable = False)
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
        return self.id
    
    def __repr__(self) :
        """
        Representation of a game.
        """
        return "<Game id : %s, gameName : %s, nbThemes : %d, nbQuestions : %d, URL : %s, creator : %s>" % (self.id, self.name, self.nbThemes, self.nbQuestions, self.URL, self.creator)


class Theme(db.Model) :
    """
    Theme class
    -------------
    Class that contains information related to the themes, that are linked to a specific game.
    """

    __tablename__ = 'theme'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    themeName = db.Column(db.String(255), nullable = False)
    #Necessity to make a link here ! 
    associatedGame = db.Column(db.String(255), nullable = False)

    def __repr__(self) :
        """
        Representation of a theme
        """
        return "<Theme id : %d, nameTheme : %s, associatedGame : %s>" % (self.id, self.nameTheme, self.associatedGame)

class Question(db.Model) :
    """
    Question class
    -----------------
    Class that contains information related to the questions, linked to a specific theme
    (and therefore a specific game too).
    """

    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
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

    def __repr__(self) :
        """
        Representation of a question.
        """
        return "<Question id : %d, enonce : %s, reponseA : %s, reponseB : %s, reponseC : %s, reponseD : %s, bonneReponse : %s, difficultyLevel : %d, nbPoints : %d, associatedTheme : %s>" % (self.id, self.enonce, self.reponseA, self.reponseB, self.reponseC, self.reponseD, self.bonneReponse, self.difficultyLevel, self.nbPoints, self.associatedTheme)


class Session(db.Model) :
    """
    Session class
    ---------------
    Class that concerns a certain session of a given game.
    This is explained by the fact that a game can be played multiple times.
    That's why we used different sessions, even tho they can concern the same game somtimes.
    """

    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #Necessity to make a link here
    gameAssociated = db.Column(db.String(255), nullable = False)
    status = db.Column(db.String(255), nullable = False)

    def __repr__(self) :
        """
        Representation of a session
        """
        return "<Session id : %d, gameAssociated : %s, status : %s>" % (self.id, self.gameAssociated, self.status)


class Answer(db.Model) :
    """
    Answer class
    ---------------
    Class that concerns the answers given by a certain player to a certain question.
    """

    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #Necessity to make a link here !!!
    usernameAssociated = db.Column(db.String(255), nullable = False)
    #Necessity to make a link here !!!
    enonce = db.Column(db.String(255), nullable = False)
    answerGiven = db.Column(db.String(255), nullable = False)
    #Necessity to make a link here !!!
    sessionAssociated = db.Column(db.String(255), nullable = False)

    def __repr__(self) :
        """
        Representation of an answer.
        """
        return "<Answer id : %d, usernameAssociated : %s, enonce : %s, answerGiven : %s, sessionAssociated : %s>" % (self.id, self.usernameAssociated, self.enonce, self.answerGiven, self.sessionAssociated)


#The DB part :
db.drop_all()
db.create_all()


#Hardcode of my user in the DB (just for convenience)
utilisateurs = Account(username = "carbonnm", lastName = "Carbonnelle", firstName = "Marie", email = "marie.carbonnelle@student.unamur.be", password = generate_password_hash("Dzhari50"))
db.session.add(utilisateurs)


#Hardcode of a very simple game to test (for convenience too)
#Simple game part
basicGame = Game(gameName = "Physique simple", nbThemes = 3, nbQuestions = 3, URL = "physique", creator = "carbonnm")
db.session.add(basicGame)

#Themes part
theme1 = Theme(themeName = "Lois de Newton", associatedGame = "Physique simple")
theme2 = Theme(themeName = "Vitesse", associatedGame = "Physique simple")
theme3 = Theme(themeName = "Ondes", associatedGame = "Physique simple")

db.session.add(theme1)
db.session.add(theme2)
db.session.add(theme3)

#Questions part
question1 = Question(enonce = "Si je pèse 70 kg et que l'on considère que la gravité vaut 10m/s2, Que vaut la force qui s'applique sur moi en ce moment ?", 
                    reponseA = "70 N", 
                    reponseB = "7000 N",
                    reponseC = "700 N", 
                    reponseD = "7 N",
                    bonneReponse = "700 N",
                    difficultyLevel = 1,
                    nbPoints = 1,
                    associatedTheme = "Lois de Newton")

question2 = Question(enonce = "Quelle est la deuxième loi de Newton", 
                    reponseA = "Tout objet non soumis à des forces conserve son état de repos ou de mouvement rectiligne et uniforme", 
                    reponseB = "F = m a",
                    reponseC = "Action et réaction: si un objet exerce une force F sur un second objet, celui-ci exerce à son tour une force -F sur le premier.", 
                    reponseD = "Les forces de frottements.",
                    bonneReponse = "F = m a",
                    difficultyLevel = 2,
                    nbPoints = 2,
                    associatedTheme = "Lois de Newton")

question3 = Question(enonce = "Quelle loi de Newton permet d'expliquer pourquoi on peut sentir les choses que l'on touche ?", 
                    reponseA = "Première loi de Newton ou principe de l'inertie.", 
                    reponseB = "Deuxième loi de Newton ou principe fondamental de la dynamique.",
                    reponseC = "Troisième loi de Newton ou principe de l'action et de la réaction.", 
                    reponseD = "Aucune des réponses ci-dessus.",
                    bonneReponse = "Troisième loi de Newton ou principe de l'action et de la réaction.",
                    difficultyLevel = 3,
                    nbPoints = 3,
                    associatedTheme = "Lois de Newton")

question4 = Question(enonce = "Quelle est lunité réglementaire de la vitesse (selon le SI) ?", 
                    reponseA = "km/h", 
                    reponseB = "(m/s)/2",
                    reponseC = "m/s", 
                    reponseD = "km/s",
                    bonneReponse = "m/s",
                    difficultyLevel = 1,
                    nbPoints = 1,
                    associatedTheme = "Vitesse")

question5 = Question(enonce = "Quelle est la formule de la vitesse ?", 
                    reponseA = "Vitesse = Distance/Temps", 
                    reponseB = "Vitesse = masse x accélération",
                    reponseC = "Vitesse = Emc2", 
                    reponseD = "Vitesse = Energie interne + Energie mécanique",
                    bonneReponse = "Vitesse = Distance/Temps",
                    difficultyLevel = 2,
                    nbPoints = 2,
                    associatedTheme = "Vitesse")

question6 = Question(enonce = "Ophélie a parcouru 62,5 km à la vitesse de 40 km/h. Quelle est la durée du trajet ? ", 
                    reponseA = "1 heure 46 minutes", 
                    reponseB = "33 minutes 45 secondes",
                    reponseC = "46 minutes et 1 seconde", 
                    reponseD = "45 minutes et 33 secondes",
                    bonneReponse = "33 minutes 45 secondes",
                    difficultyLevel = 3,
                    nbPoints = 3,
                    associatedTheme = "Vitesse")

question7 = Question(enonce = "Quelles sont les ondes produites lorsqu'on téléphone ?", 
                    reponseA = "Des ondes gravitationnelles", 
                    reponseB = "Des ondes sonores",
                    reponseC = "Des ondes sysmiques", 
                    reponseD = "Des ondes radios",
                    bonneReponse = "Des ondes radios",
                    difficultyLevel = 1,
                    nbPoints = 1,
                    associatedTheme = "Ondes")

question8 = Question(enonce = "Lequel utilise les longueurs d'ondes les plus courtes ?", 
                    reponseA = "L'infrarouge", 
                    reponseB = "La lumière visible",
                    reponseC = "L'ultraviolet", 
                    reponseD = "La lumière bleue",
                    bonneReponse = "L'ultraviolet",
                    difficultyLevel = 2,
                    nbPoints = 2,
                    associatedTheme = "Ondes")

question9 = Question(enonce = "Quel type d'ondes émet la chauve-souris pour se déplacer ?", 
                    reponseA = "Des ultrasons", 
                    reponseB = "De l'infrarouge",
                    reponseC = "De l'électromagnétique", 
                    reponseD = "De l'ultraviolet",
                    bonneReponse = "Des ultrasons",
                    difficultyLevel = 3,
                    nbPoints = 3,
                    associatedTheme = "Ondes")

db.session.add(question1)
db.session.add(question2)
db.session.add(question3)
db.session.add(question4)
db.session.add(question5)
db.session.add(question6)
db.session.add(question7)
db.session.add(question8)
db.session.add(question9)

db.session.commit()



# callback to reload the user object
@login_manager.user_loader
def load_user(userID):
    return Account.query.get(int(userID))