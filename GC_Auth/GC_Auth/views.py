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



# READ methods

# ToDo: read badges for profile


def getUsername(request, user):
    name = database.child('Users').child(user['localId']).child('Name').get()
    return name.val()


def getBio(request, user):
    return database.child('Users').child(user['localId']).child('Bio').get().val()


def getCountry(request, user):
    return database.child('Users').child(user['localId']).child('Country').get().val()


def getNumConnecions(request, user):
    return database.child('Users').child(user['localId']).child('numConnections').get().val()


def getNumForums(request, user):
    return database.child('Users').child(user['localId']).child('numForums').get().val()


def getProfilePic(request, user):
    return database.child('Users').child(user['localId']).child('ProfilePic').get().val()


def getBackgroundPic(request, user):
    return database.child('Users').child(user['localId']).child('BackgroundPic').get().val()

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

    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
        global u
        u = user
    except:
        message = "invalid credentials"
        return render(request, "LogIn.html", {"messg": message})
    print(user['localId'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    return render(request, "UserProfile.html", {"e": email,
                                                'n': getUsername(request, user),
                                                'bio': getBio(request, user),
                                                'email': email,
                                                'country': getCountry(request, user),
                                                'numConnections': getNumConnecions(request, user),
                                                'numForums': getNumForums(request, user),
                                                'ProfilePic': getProfilePic(request, user),
                                                'backgroundPic': getBackgroundPic(request, user)})


def logout(request):
    auth.logout(request)
    return render(request, 'LogIn.html')


def signUp(request):
    return render(request, "signup.html")


def postsignup(request):
    global r
    r = request

    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        global u
        u = user
        uid = user['localId']
        data = {"name": name, "status": "1"}
        database.child("users").child(uid).child("details").set(data)
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", {"messg": message})

    return render(request, "signIn.html")


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
    updateUsername(name)
    updateBio(bio)
    updateCountry(country)
    updateProfilePic(pPic)
    updateBackgroundPic(bPic)

    # edit return render to show the new data
    return render(request, "UserProfile.html", {'n': name,
                                                'bio': bio,
                                                'country': country,
                                                'ProfilePic': pPic,
                                                'backgroundPic': bPic
                                                })


def updateUsername(name):
    database.child("Users").child(u['localId']).update({"Name": name})


def updateBio(bio):
    database.child("Users").child(u['localId']).update({"Bio": bio})


def updateCountry(country):
    database.child("Users").child(u['localId']).update({"Country": country})


def updateProfilePic(pPic):
    database.child("Users").child(u['localId']).update({"ProfilePic": pPic})


def updateBackgroundPic(bPic):
    database.child("Users").child(u['localId']).update({"BackgroundPic": bPic})


def updateBadge():
    # ToDo: create method to update badges in DB - not used in UI
    return ""

# ToDo: test update methods

def updatePrivacySettings(request):
    # ToDo: code to update privacy settings - similar to update profile code
    return ""


# ToDo: code to change password - verify through user email

# ToDo: code to add ratings to courses

