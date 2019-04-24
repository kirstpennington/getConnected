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

r = ""  # request
u = ""  # user
email = ""
password = ""

# READ methods

# ToDo: read badges for profile

def getProfileData(request):
    return render(request, "UserProfile.html", {"e": r.POST.get('email'),
                                                'n': getUsername(u),
                                                'bio': getBio(r, u),
                                                'email': r.POST.get('email'),
                                                'country': getCountry(u),
                                                'numConnections': getNumConnecions(r, u),
                                                'numForums': getNumForums(r, u),
                                                'ProfilePic': getProfilePic(r, u),
                                                'backgroundPic': getBackgroundPic(r, u)})


def getPrivacySettings(request):
    # Name of html file to be changed
    return render(request, "PrivacySettings.html", {'bioPrivacy': getBioPrivacy(u),
                                                'connectionPrivacy': getConnectionPrivacy(u),
                                                'countryPrivacy': getCountryPrivacy(u),
                                                'namePrivacy': getNamePrivacy(u),
                                                'pPicPrivacy': getPicPrivacy(u),
    })

     # individual get methods


def getUsername(user):
    name = database.child('Users').child(user['localId']).child('Name').get()
    return name.val()


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
    global r
    r = request

    global email
    email = request.POST.get('email')

    global password
    password = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email, password)
        global u
        u = user
    except:
        message = "Incorrect Username or Password"
        return render(request, "LogIn.html", {"messg": message})
    print(user['localId'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    if getBackgroundPic(request, user) == "":
        updateBackgroundPic("https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg")

    if getProfilePic(request, user) == "":
        updateProfilePic("https://i.kinja-img.com/gawker-media/image/upload/s--hgzsnuUb--/c_scale,f_auto,fl_progressive,q_80,w_800/kwzzpvj7b7f8kc8lfgz3.jpg")

    return render(request, "UserProfile.html", {"e": email,
                                                'n': getUsername(user),
                                                'bio': getBio(request, user),
                                                'email': email,
                                                'country': getCountry(user),
                                                'numConnections': getNumConnecions(request, user),
                                                'numForums': getNumForums(request, user),
                                                'ProfilePic': getProfilePic(request, user),
                                                'backgroundPic': getBackgroundPic(request, user)})


def logout(request):
    auth.logout(request)
    return render(request, 'LogIn.html')



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


# UPDATE Methods

def updateProfile(request):

    if request.method == "POST":
        # get data from UI using POST method
        name = request.POST.get("name")
        bio = request.POST.get("bio")
        country = request.POST.get("country")
        pPic = request.POST.get("pPic")
        bPic = request.POST.get("bPic")
        # ToDo: use the naming conventions in the get() method in the UI - name="name"; name="bio"; name="country"

    # call each method to update elements of the profile in the db
    updateUsername(u, name)
    updateBio(u, bio)
    updateCountry(u, country)
    updateProfilePic(u, pPic)
    updateBackgroundPic(u, bPic)

    # edit return render to show the new data
    return render(request, "UserProfile.html", {'n': name,
                                                'bio': bio,
                                                'country': country,
                                                'ProfilePic': pPic,
                                                'backgroundPic': bPic
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
    database.child("Users").child(user['localId']).update({"Name": name})


def updateBio(user, bio):
    database.child("Users").child(user['localId']).update({"Bio": bio})


def updateCountry(user, country):
    database.child("Users").child(user['localId']).update({"Country": country})


def updateProfilePic(user, pPic):
    database.child("Users").child(user['localId']).update({"ProfilePic": pPic})


def updateBackgroundPic(user, bPic):
    database.child("Users").child(user['localId']).update({"BackgroundPic": bPic})


def updateBadge():
    # ToDo: create method to update badges in DB - not used in UI
    return ""


def updateBioPrivacy(user, bioPrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"BioPrivacy": bioPrivacy})


def updateConnectionPrivacy(user, connectionPrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"ConnectionPrivacy": connectionPrivacy})


def updateCountryPrivacy(user, countryPrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"CountryPrivacy": countryPrivacy})


def updateNamePrivacy(user, namePrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"NamePrivacy": namePrivacy})


def updatePicPrivacy(user, pPicPrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"ProfilePicPrivacy": pPicPrivacy})


# ToDo: code to add ratings to courses


#Navigation bar functionality

def home(request):
    return render(request, 'UserProfile.html')

def networks(request):
    return render(request, 'MyNetwork.html')

def forums(request):
    return render(request, 'Forums.html')

def courses(request):
    return render(request, 'Courses.html')

def userprofile(request):
    return render(request, 'UserProfile.html')

