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
                                                'n': getUsername(r, u),
                                                'bio': getBio(r, u),
                                                'email': r.POST.get('email'),
                                                'country': getCountry(r, u),
                                                'numConnections': getNumConnecions(r, u),
                                                'numForums': getNumForums(r, u),
                                                'ProfilePic': getProfilePic(r, u),
                                                'backgroundPic': getBackgroundPic(r, u)})


def getPrivacySettings(request):
    # Name of html file to be changed
    return render(request, "PrivacySettings.html", {'bioPrivacy': getBioPrivacy(),
                                                'connectionPrivacy': getConnectionPrivacy(),
                                                'countryPrivacy': getCountryPrivacy(),
                                                'namePrivacy': getNamePrivacy(),
                                                'pPicPrivacy': getPicPrivacy(),
    })

     # individual get methods

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


def getBioPrivacy():
    database.child("Users").child(u['localId']).child("UserPrivacy").child("BioPrivacy").get().val()


def getConnectionPrivacy():
    database.child("Users").child(u['localId']).child("UserPrivacy").child("ConnectionPrivacy").get().val()


def getCountryPrivacy():
    database.child("Users").child(u['localId']).child("CountryPrivacy").child("BioPrivacy").get().val()


def getNamePrivacy():
    database.child("Users").child(u['localId']).child("UserPrivacy").child("NamePrivacy").get().val()


def getPicPrivacy():
    database.child("Users").child(u['localId']).child("ProfilePicPrivacy").child("BioPrivacy").get().val()

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
    updateBioPrivacy(bioPrivacy)
    updateConnectionPrivacy(connectionPrivacy)
    updateCountryPrivacy(countryPrivacy)
    updateNamePrivacy(namePrivacy)
    updatePicPrivacy(pPicPrivacy)

    # edit return render to show the new data
    return render(request, "UserProfile.html", {'bioPrivacy': bioPrivacy,
                                                'connectionPrivacy': connectionPrivacy,
                                                'countryPrivacy': countryPrivacy,
                                                'namePrivacy': namePrivacy,
                                                'pPicPrivacy': pPicPrivacy
                                                })
    # individual update methods

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


def updateBioPrivacy(bioPrivacy):
    database.child("Users").child(u['localId']).child("UserPrivacy").update({"BioPrivacy": bioPrivacy})


def updateConnectionPrivacy(connectionPrivacy):
    database.child("Users").child(u['localId']).child("UserPrivacy").update({"ConnectionPrivacy": connectionPrivacy})


def updateCountryPrivacy(countryPrivacy):
    database.child("Users").child(u['localId']).child("UserPrivacy").update({"CountryPrivacy": countryPrivacy})


def updateNamePrivacy(namePrivacy):
    database.child("Users").child(u['localId']).child("UserPrivacy").update({"NamePrivacy": namePrivacy})


def updatePicPrivacy(pPicPrivacy):
    database.child("Users").child(u['localId']).child("UserPrivacy").update({"ProfilePicPrivacy": pPicPrivacy})


# ToDo: code to add ratings to courses



