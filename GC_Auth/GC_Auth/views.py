from django.http import HttpResponseRedirect
from django.shortcuts import render
import pyrebase
from django.contrib import  auth

config = {

    'apiKey': "AIzaSyCW2DTUu_qEhCG9xpj5gGkG2_QC_CmsGQE",
    'authDomain': "getconnected-9dac0.firebaseapp.com",
    'databaseURL': "https://getconnected-9dac0.firebaseio.com",
    'projectId': "getconnected-9dac0",
    'storageBucket': "getconnected-9dac0.appspot.com",
    'messagingSenderId': "144309081376"
}


# global variables
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

r = ""  # store initial user request for authentication
u = ""  # store user variable for Firebase authentication

the_user = ""       # object to store user information
user_privacy = ""   # object to store user privacy information

# READ methods

# ToDo: read badges for profile


def getPrivacySettings(request):
    # Name of html file to be changed
        return render(request, "PrivacySettings.html", {'bioPrivacy': user_privacy.bio,
                                                'connectionPrivacy': user_privacy.connections,
                                                'countryPrivacy': user_privacy.country,
                                                'namePrivacy': user_privacy.name,
                                                'pPicPrivacy': user_privacy.pic,
        })



     # individual get methods - these methods are only used when the user signs in. Otherwise, data is taken from the the_user object


def getUsername(user):
    return database.child('Users').child(user['localId']).child('Name').get().val()


def getBio(request, user):
    return database.child('Users').child(user['localId']).child('Bio').get().val()


def getCountry(user):
    return database.child('Users').child(user['localId']).child('Country').get().val()


def getNumConnecions(request, user):
    return database.child('Users').child(user['localId']).child('numConnections').get().val()


def getNumForums(request, user):
    return database.child('Users').child(user['localId']).child('numForums').get().val()


def getProfilePic(request, user):
    return database.child('Users').child(user['localId']).child('ProfilePic').get().val()


def getBackgroundPic(request, user):
    return database.child('Users').child(user['localId']).child('BackgroundPic').get().val()


def getBioPrivacy(user):
    return database.child("Users").child(user['localId']).child("UserPrivacy").child("BioPrivacy").get().val()


def getConnectionPrivacy(user):
    return database.child("Users").child(user['localId']).child("UserPrivacy").child("ConnectionPrivacy").get().val()


def getCountryPrivacy(user):
    return database.child("Users").child(user['localId']).child("UserPrivacy").child("CountryPrivacy").get().val()


def getNamePrivacy(user):
    return database.child("Users").child(user['localId']).child("UserPrivacy").child("NamePrivacy").get().val()


def getPicPrivacy(user):
    return database.child("Users").child(user['localId']).child("UserPrivacy").child("ProfilePicPrivacy").get().val()

# ToDo: code to get data for forums and courses in carousels - list of data

# ToDo: read course info for Courses page

# ToDo: find recommended courses for Courses page



# LOGIN methods

def LogIn(request):
    return render(request, "LogIn.html")


def passwordReset(request):

    # ... your python code/script
    return render(request,"passwordReset.html")


def postsign(request):

    # user authentication with Firebase
    global r
    r = request

    email = request.POST.get('email')
    password = request.POST.get("pass")

    try:
        user = authe.sign_in_with_email_and_password(email, password)
        global u
        u = user
    except:
        message = "Incorrect Username or Password"
        return render(request, "LogIn.html", {"messg": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    # if the user image or background is blank, set it to a default value
    if getBackgroundPic(request, user) == "":
        updateBackgroundPic("https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg")

    if getProfilePic(request, user) == "":
        updateProfilePic("https://i.kinja-img.com/gawker-media/image/upload/s--hgzsnuUb--/c_scale,f_auto,fl_progressive,q_80,w_800/kwzzpvj7b7f8kc8lfgz3.jpg")

    global the_user # create the_user object to store user profile data
    the_user = User(getUsername(user), getBio(request, user), getNumConnecions(request, user), getNumForums(request, user), email, password, getCountry(user), getProfilePic(request, user),getBackgroundPic(request, user))

    global user_privacy # create user_privacy object to store user privacy data
    user_privacy = Privacy(getBioPrivacy(user), getConnectionPrivacy(user), getCountryPrivacy(user), getNamePrivacy(user), getPicPrivacy(user))

    # navigate to the user profile page and
    return render(request, "UserProfile.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic':the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic})


def logout(request):
    auth.logout(request)
    return render(request, 'LogIn.html')


# UPDATE Methods

def updateProfile(request):

    if request.method == "POST":
        # get data from UI using POST method
        name = request.POST.get("name")
        bio = request.POST.get("bio")
        country = request.POST.get("country")

        # ToDo: use the naming conventions in the get() method in the UI - name="name"; name="bio"; name="country"

    # call each method to update elements of the profile in the db
    updateUsername(u, name)
    updateBio(u, bio)
    updateCountry(u, country)

    # edit return render to show the new data
    return render(request, "UserProfile.html", {'n': name,
                                                'bio': bio,
                                                'country': country,
                                                'ProfilePic': the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic,
                                                })


def updatePrivacySettings(request):
    if request.method == "POST":
        # get data from UI using POST method
        bioPrivacy = request.POST.get("bioPrivacy")
        connectionPrivacy = request.POST.get("connectionPrivacy")
        countryPrivacy = request.POST.get("countryPrivacy")
        namePrivacy = request.POST.get("namePrivacy")
        pPicPrivacy = request.POST.get("pPicPrivacy")
        # ToDo: use the naming conventions in the get() method in the UI - name="name"; name="bio"; name="country"

    # call each method to update elements of the profile in the db
    updateBioPrivacy(u, bioPrivacy)
    updateConnectionPrivacy(u, connectionPrivacy)
    updateCountryPrivacy(u, countryPrivacy)
    updateNamePrivacy(u, namePrivacy)
    updatePicPrivacy(u, pPicPrivacy)

    # edit return render to show the new data
    return render(request, "UserProfile.html", {'bioPrivacy': bioPrivacy,
                                                'connectionPrivacy': connectionPrivacy,
                                                'countryPrivacy': countryPrivacy,
                                                'namePrivacy': namePrivacy,
                                                'pPicPrivacy': pPicPrivacy
                                                })
    # individual update methods


def updateUsername(user, name):
    database.child("Users").child(user['localId']).update({"Name": name})   # update element in the database
    try:  # try except for purpose of unit tests
        global the_user
        the_user.username = name        # update element in the local object
    except:
        return ""


def updateBio(user, bio):
    database.child("Users").child(user['localId']).update({"Bio": bio})
    try:  # try except for purpose of unit tests
        global the_user
        the_user.bio = bio
    except:
        return ""


def updateCountry(user, country):
    database.child("Users").child(user['localId']).update({"Country": country})
    try:  # try except for purpose of unit tests
        global the_user
        the_user.username = country
    except:
        return ""


def updateProfilePic(user, pPic):
    database.child("Users").child(user['localId']).update({"ProfilePic": pPic})
    try:  # try except for purpose of unit tests
        global the_user
        the_user.profilePic = pPic
    except:
        return ""


# method for updating only the profile pic
def updateProfilePicRequest(request):

    # get data from UI
    if request.method == "POST":
        # get data from UI using POST method
        newPic = request.POST.get("newPic")

    # edit the object value for profile pic
    global the_user
    the_user.profilePic = newPic

    # set new profile pic in DB
    database.child("Users").child(u['localId']).update({"ProfilePic": newPic})
    return render(request, "UserProfile.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic': the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic})

# method for updating only the background pic
def updateBackgroundPicRequest(request):

    # get data from UI
    if request.method == "POST":
        # get data from UI using POST method
        newPic = request.POST.get("newPic")

    # edit the object value for profile pic
    global the_user
    the_user.backgroundPic = newPic

    # set new profile pic in DB
    database.child("Users").child(u['localId']).update({"BackgroundPic": newPic})
    return render(request, "UserProfile.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic': the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic})


def updateBackgroundPic(user, bPic):
    database.child("Users").child(user['localId']).update({"BackgroundPic": bPic})
    try: # try except for purpose of unit tests
        global the_user
        the_user.backgroundPic = bPic
    except:
        return ""


def updateBadge():
    # ToDo: create method to update badges in DB - not used in UI
    return ""


def updateBioPrivacy(user, bioPrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"BioPrivacy": bioPrivacy})
    try:  # try except for purpose of unit tests
        global user_privacy
        user_privacy.bio = bioPrivacy
    except:
        return ""


def updateConnectionPrivacy(user, connectionPrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"ConnectionPrivacy": connectionPrivacy})
    try:  # try except for purpose of unit tests
        global user_privacy
        user_privacy.connections = connectionPrivacy
    except:
        return ""


def updateCountryPrivacy(user, countryPrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"CountryPrivacy": countryPrivacy})
    try:  # try except for purpose of unit tests
        global user_privacy
        user_privacy.country = countryPrivacy
    except:
        return ""


def updateNamePrivacy(user, namePrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"NamePrivacy": namePrivacy})
    try:
        global user_privacy
        user_privacy.name = namePrivacy
    except:
        return ""


def updatePicPrivacy(user, pPicPrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"ProfilePicPrivacy": pPicPrivacy})
    try:  # try except for purpose of unit tests
        global user_privacy
        user_privacy.pic = pPicPrivacy
    except:
        return ""


# ToDo: code to add ratings to courses


# Navigation Methods

def home(request):
     return render(request, "UserProfile.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic': the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic})


def networks(request):
    return render(request, 'MyNetwork.html')


def forums(request):
    return render(request, 'Forums.html')


def courses(request):
    return render(request, 'Courses.html')


def userprofile(request):
    return render(request, "UserProfile.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic': the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic})

def goSettings(request):
    return render(request, "Setttings.html")


def goBadges(request):
    return render(request, "badgesStart.html")


def goHelpUserProfile(request):
    return render(request, "helpUserProfile.html")


def goIntroHelp(request):
    return render(request, 'introducingHelp.html')


def goAccountHelp(request):
    return render(request, 'accountHelp.html')


def goForumsOpen(request):
    return render(request, 'ForumsOpen.html')


def goSettings(request):
    return render(request, 'Setttings.html')


def goContact(request):
    return render(request, 'contactus.html')


# these objects only store info that the user updates manually-info that is not constantly being updates
# class with user profile info
class User:
    def __init__(self, name, bio, numConn, numForum, em, pa, country, profPic, bPic, ):
        self.username = name
        self.bio = bio
        self.numConnections = numConn
        self.numForums = numForum
        self.email = em
        self.password = pa
        self.country = country
        self.profilePic = profPic
        self.backgroundPic = bPic


# class with user privacy info
class Privacy:
    def __init__(self, bio, connections, country, name, pic):
        self.bio = bio
        self.connections = connections
        self.country = country
        self.name = name
        self.pic = pic

