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

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()

#  Badges, profilePic, courses, forums


# READ methods


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

# LOGIN methods


def LogIn(request):
    return render(request, "LogIn.html")


def passwordReset(request):

    # ... your python code/script
    return render(request,"passwordReset.html")


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
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
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
        data = {"name": name, "status": "1"}
        database.child("users").child(uid).child("details").set(data)
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", {"messg": message})

    return render(request, "signIn.html")



