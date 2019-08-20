from django.http import HttpResponseRedirect
from django.shortcuts import render
import pyrebase
from django.contrib import auth
from GC_Auth.Privacy import Privacy
from GC_Auth.User import User


# stores all methods related to courses

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

class user_methods:
    # GET Methods
    def getUsername(uid):
        return database.child('Users').child(uid).child('Name').get().val()

    def getBio(uid):
        return database.child('Users').child(uid).child('Bio').get().val()

    def getCountry(uid):
        return database.child('Users').child(uid).child('Country').get().val()

    def getNumConnecions(uid):
        return database.child('Users').child(uid).child('numConnections').get().val()

    def getNumForums(uid):
        temp = database.child('Users').child(uid).child('numForums').get().val()
        if temp is None:
            return 0
        else:
            return int(temp)

    def getNumCourses(uid):
        return int(database.child('Users').child(uid).child('numCourses').get().val())

    def getPrivacyUpdated(uid):
        return database.child('Users').child(uid).child('privacyUpdated').get().val()

    def getProfilePic(uid):
        return database.child('Users').child(uid).child('ProfilePic').get().val()

    def getProfilePic(uid):
        return database.child('Users').child(uid).child('ProfilePic').get().val()

    def getBackgroundPic(uid):
        return database.child('Users').child(uid).child('BackgroundPic').get().val()

    def getBioPrivacy(uid):
        return database.child("Users").child(uid).child("UserPrivacy").child("BioPrivacy").get().val()

    def getConnectionPrivacy(uid):
        return database.child("Users").child(uid).child("UserPrivacy").child("ConnectionPrivacy").get().val()

    def getCountryPrivacy(uid):
        return database.child("Users").child(uid).child("UserPrivacy").child("CountryPrivacy").get().val()

    def getNamePrivacy(uid):
        return database.child("Users").child(uid).child("UserPrivacy").child("NamePrivacy").get().val()

    def getPicPrivacy(uid):
        return database.child("Users").child(uid).child("UserPrivacy").child("ProfilePicPrivacy").get().val()

    def getCoursesPrivacy(uid):
        return database.child("Users").child(uid).child("UserPrivacy").child("CoursesPrivacy").get().val()

    def getForumsPrivacy(uid):
        return database.child("Users").child(uid).child("UserPrivacy").child("ForumsPrivacy").get().val()

    def getUserConnectionsList(uid):
        return database.child("Users").child(uid).child("Connections").shallow().get().val()

    def getUpdatedProfilePic(uid):
        return database.child("Users").child(uid).child("updatedProfilePic").get().val()

    def getUpdatedPrivacySettings(uid):
        return database.child("Users").child(uid).child("privacyUpdated").get().val()

    # for filling the Courses blocks
    def getCoursesList(uid):
        # get list of courses IDs that a user takes
        # code from : https://www.hackanons.com/2018/05/python-django-with-google-firebase_31.html
        course_ids = database.child('Users').child(uid).child('Courses').shallow().get().val()
        course_id_list = []  # stores list of course ids for the user
        if course_ids is None:
            return []
        else:
            for i in course_ids:
                course_id_list.append(i)
            return course_id_list

    # gets a list of the forums in the order that the user visited them
    # when a forum is visited, it is added to the top of the db tree and the last forum in the tree in removed - tree always contains top 3 recently visited forums
    def getForumssList(uid):
        # get list of forum IDs that a user takes
        # code from : https://www.hackanons.com/2018/05/python-django-with-google-firebase_31.html
        forum_ids = database.child('Users').child(uid).child('ForumVisits').shallow().get().val()
        forum_id_list = []  # stores list of course ids for the user
        if forum_ids is None:
            return []
        else:
            for i in forum_ids:
                forum_id_list.append(i)

            return forum_id_list

    def getUserTopicsList(uid):
        # get this user's interests/topics in a list
        return database.child("Users").child(uid).child("Topics").shallow().get().val()


    # UPDATE Methods

    def updateUsername(uid, name):
        database.child("Users").child(uid).update({"Name": name})  # update element in the database
        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def updateEmail(uid, e):
        # insert code to update email address (optional)
        try:
            return ""
        except:
            return ""

    def updateBio(uid, bio):
        database.child("Users").child(uid).update({"Bio": bio})
        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def updateCountry(uid, country):
        database.child("Users").child(uid).update({"Country": country})
        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def updateProfilePic(uid, pPic):
        database.child("Users").child(uid).update({"ProfilePic": pPic})
        if user_methods.getUpdatedProfilePic(uid) != "yes":                 # tracks whether the user has updated their profile pic before for awarding badges
            user_methods.updateUpdatedProfilePic(uid)
        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def updateBackgroundPic(uid, bPic):
        database.child("Users").child(uid).update({"BackgroundPic": bPic})
        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def deleteProfilePic(uid):
        user_methods.updateProfilePic(uid, "https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg")

    def deleteBackgroundPic(uid):
        user_methods.updateBackgroundPic(uid,
                            "https://cdn.shopify.com/s/files/1/2656/8500/products/galerie-wallpapers-unplugged-textured-plain-grey-wallpaper-2035691716651_1024x.jpg?v=1522251583")

    def updateBioPrivacy(uid, bioPrivacy):
        database.child("Users").child(uid).child("UserPrivacy").update({"BioPrivacy": bioPrivacy})

        if user_methods.getUpdatedPrivacySettings(
                uid) != "yes":  # tracks whether the user has updated their profile pic before for awarding badges
            user_methods.updateUpdatedPrivacySettings(uid)

        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def updateConnectionPrivacy(uid, connectionPrivacy):
        database.child("Users").child(uid).child("UserPrivacy").update(
            {"ConnectionPrivacy": connectionPrivacy})

        if user_methods.getUpdatedPrivacySettings(
                uid) != "yes":  # tracks whether the user has updated their profile pic before for awarding badges
            user_methods.updateUpdatedPrivacySettings(uid)

        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def updateCountryPrivacy(uid, countryPrivacy):
        database.child("Users").child(uid).child("UserPrivacy").update({"CountryPrivacy": countryPrivacy})

        if user_methods.getUpdatedPrivacySettings(
                uid) != "yes":  # tracks whether the user has updated their profile pic before for awarding badges
            user_methods.updateUpdatedPrivacySettings(uid)

        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def updateNamePrivacy(uid, namePrivacy):
        database.child("Users").child(uid).child("UserPrivacy").update({"NamePrivacy": namePrivacy})

        if user_methods.getUpdatedPrivacySettings(
                uid) != "yes":  # tracks whether the user has updated their profile pic before for awarding badges
            user_methods.updateUpdatedPrivacySettings(uid)

        try:
            return ""
        except:
            return ""

    def updatePicPrivacy(uid, pPicPrivacy):
        database.child("Users").child(uid).child("UserPrivacy").update({"ProfilePicPrivacy": pPicPrivacy})

        if user_methods.getUpdatedPrivacySettings(
                uid) != "yes":  # tracks whether the user has updated their profile pic before for awarding badges
            user_methods.updateUpdatedPrivacySettings(uid)

        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def updateCoursesPrivacy(uid, coursesPrivacy):
        database.child("Users").child(uid).child("UserPrivacy").update({"CoursesPrivacy": coursesPrivacy})

        if user_methods.getUpdatedPrivacySettings(
                uid) != "yes":  # tracks whether the user has updated their profile pic before for awarding badges
            user_methods.updateUpdatedPrivacySettings(uid)

        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def updateForumsPrivacy(uid, forumsPrivacy):
        database.child("Users").child(uid).child("UserPrivacy").update({"ForumsPrivacy": forumsPrivacy})

        if user_methods.getUpdatedPrivacySettings(
                uid) != "yes":  # tracks whether the user has updated their profile pic before for awarding badges
            user_methods.updateUpdatedPrivacySettings(uid)

        try:  # try except for purpose of unit tests
            return ""
        except:
            return ""

    def updateUpdatedProfilePic(uid):
        database.child("Users").child(uid).update({"updatedProfilePic": "yes"})

    def updateUpdatedPrivacySettings(uid):
        database.child("Users").child(uid).update({"privacyUpdated": "yes"})
