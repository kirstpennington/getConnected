from django.http import HttpResponseRedirect
from django.shortcuts import render
import pyrebase
from django.contrib import auth
from GC_Auth.Privacy import Privacy
from GC_Auth.User import User
from GC_Auth.users import user_methods

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

class connection_methods:

# GET Methods
    def getConnectionsInfoList(connections_id_list):
        names = []
        countries = []
        pictures = []
        bio = []
        conn_id = []

        for id in connections_id_list:
            if user_methods.getNamePrivacy(
                    id) == "False":  # checks the user's privacy settings before displaying it in the suggestion
                names.append(user_methods.getUsername(id))
            else:
                names.append("User's Name Private")

            if user_methods.getCountryPrivacy(
                    id) == "False":  # checks the user's privacy settings before displaying it in the suggestion
                countries.append(user_methods.getCountry(id))
            else:
                countries.append("User's Country Private")

            if user_methods.getPicPrivacy(
                    id) == "False":  # checks the user's privacy settings before displaying it in the suggestion
                pictures.append(user_methods.getProfilePic(id))
            else:
                pictures.append("https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg")

            if user_methods.getBioPrivacy(id) == "False" or user_methods.getBioPrivacy(id) == "false":
                bio.append(user_methods.getBio(id))
            else:
                bio.append("Bio Private")

            conn_id.append(id)

        return zip(names, countries, pictures, bio, conn_id)

    def getConnectionsSuggestions(uid, num_returns, the_user):
        # returns a combined list of user information with the same interests as this user
        results_count = 0  # how many results were found thus far
        results = []

        all_users_list_1 = database.child("Users").shallow().get().val()  # list of all users in the system
        all_users_list = connection_methods.removeValueFromList(uid, all_users_list_1)  # remove this user from the list of all users
        for compare_user_id in all_users_list:
            if results_count == num_returns:  # if we have the requested number of ids, stop searching
                break
            else:
                # get the topics of the user we are currently comparing this user wih
                compare_user_interests = database.child("Users").child(compare_user_id).child(
                    "Topics").shallow().get().val()
                if connection_methods.compareLists(compare_user_interests,
                                the_user.topicsList):  # if we find a match, add it to the list of results
                    results.append(compare_user_id)
                    results_count += 1

        user_connections_list = database.child("Users").child(uid).child(
            'Connections').shallow().get().val()  # get list of this user connections
        final_results = connection_methods.removeValuesFromList(user_connections_list,
                                             results)  # remove users that are already connections and return this updated list

        return connection_methods.getConnectionsInfoList(final_results)


    # supporting methods for finding suggestions
    def removeCommons(remove_from_this_list, search_this_list):
        # removes the common values between the 2 lists from the first list
        temp = []  # dummy variable where items from the list will be removed
        for r in remove_from_this_list:
            for s in search_this_list:
                if r != s:
                    temp.append(r)
        return temp


    # converts a python dictionary to a list
    def convertDictToList(dict):
        temp = []
        for key, value in dict.items():
            temp.append(key)
        return temp


    def removeValuesFromList(values_list, main_list):
        temp = []
        for m in main_list:
            add = True
            for v in values_list:
                if m == v:
                    add = False
                    break
            if add:
                temp.append(m)
        return temp


    def removeValueFromList(value, list):
        temp = []
        for li in list:
            if li != value:
                temp.append(li)
        return temp


    def compareLists(list1, list2):
        # returns true if there are matching values in the 2 lists
        for a in list1:
            for b in list2:
                if a == b:
                    return True
        return False
