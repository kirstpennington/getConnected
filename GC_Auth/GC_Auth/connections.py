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
    def getUserEnabled(uid):
        return database.child("Users").child(uid).child("Enabled").get().val()

    def getConnectionsInfoList(connections_id_list):
        names = []
        countries = []
        pictures = []
        bio = []
        conn_id = []

        if connections_id_list is not None:
            for id in connections_id_list:
                names.append(user_methods.getUsername(id))

                if user_methods.getCountryPrivacy(
                        id) == "True":  # checks the user's privacy settings before displaying it in the suggestion
                    countries.append("User's Country Private")
                else:
                    countries.append(user_methods.getCountry(id))

                pictures.append(user_methods.getProfilePic(id))

                if user_methods.getBioPrivacy(id) == "True" or user_methods.getBioPrivacy(id) == "true":
                    bio.append("Bio Private")
                else:
                    bio.append(user_methods.getBio(id))

                conn_id.append(id)

        return zip(names, countries, pictures, bio, conn_id)

    def getConnectionsSuggestions(uid, num_returns, the_user):
                                                                                                                        # returns a combined list of user information with the same interests as this user
        results_count = 0                                                                                               # how many results were found thus far
        results = []

        all_users_list_1 = database.child("Users").shallow().get().val()                                                # list of all users in the system
        all_users_list = connection_methods.removeValueFromList(uid, all_users_list_1)                                  # remove this user from the list of all users
        user_connections_list = database.child("Users").child(uid).child('Connections').shallow().get().val()           # get list of this user connections

        for compare_user_id in all_users_list:
            if results_count == num_returns:                                                                            # if we have the requested number of ids, stop searching
                break
            else:
                if the_user.uid != compare_user_id:                                                                     # remove my id from the list of results
                    if connection_methods.arrayContainsValue(connection_methods.getRequestsReceived(uid), compare_user_id) == False:            # remove users who the person has already received requests from
                        if connection_methods.arrayContainsValue(connection_methods.getRequestsSent(uid), compare_user_id) == False:            # remove the users who I have already sent connections to
                            if connection_methods.arrayContainsValue(user_connections_list, compare_user_id) == False:  # remove users that are already connections
                                user_enabled = connection_methods.getUserEnabled(compare_user_id)
                                if user_enabled == 'true' or user_enabled == True:                       # only add to the list of commections if the connection's account is enabled
                                    # get the topics of the user we are currently comparing this user wih
                                    compare_user_interests = database.child("Users").child(compare_user_id).child(
                                        "Topics").shallow().get().val()
                                    if connection_methods.compareLists(compare_user_interests,
                                                    the_user.topicsList):                                               # if we find a match, add it to the list of results
                                        results.append(compare_user_id)
                                        results_count += 1

        if results is None:
            return []
        else:
            return results


    def getMutualConnections(connection_id, my_id):
        # get mutual connections and check if this user is a connection
        selected_user_connections = user_methods.getUserConnectionsList(
            connection_id)  # get a list of the selected user's connections
        logged_in_user_connections = user_methods.getUserConnectionsList(
            my_id)  # get the connections of the user who is logged in
        mutual_connections = []

        if selected_user_connections is not None:
            for connection in selected_user_connections:
                if connection_methods.arrayContainsValue(logged_in_user_connections,
                                                    connection):  # if this connection is in the logged iin user's connections list
                    mutual_connections.append(connection)
                elif connection == my_id:  # check if the user logged in is a connect
                    the_user_is_connection = True

        return mutual_connections


    def getRequestsSent(uid):     # get a list of the users who I have sent requests to (their user ids)
        sent_ids = database.child("Users").child(uid).child("RequestsSent").shallow().get().val()       # get a list of the auto generated ids for sent logs
        sent_user_ids = []

        if sent_ids is not None:
            for sent_id in sent_ids:                                                                        # search through that list for the user ids of each
                sent_user_ids.append(sent_id)


        return sent_user_ids

    def getRequestsReceived(uid):    # get a list of the users who hav sent me connection requests (their user ids)
        received_ids = database.child("Users").child(uid).child("RequestsReceived").shallow().get().val()   # get a list of the auto generated ids for received logs
        rec_user_ids = []

        if received_ids is not None:
            for rec_id in received_ids:                                                                     # search through that list for the user ids of each
                rec_user_ids.append(rec_id)

        return rec_user_ids


        # supporting methods for finding suggestions
    def removeCommons(remove_from_this_list, search_this_list):
            # removes the common values between the 2 lists from the first list
            temp = []  # dummy variable where items from the list will be removed
            if remove_from_this_list is not None and search_this_list is not None:
                for r in remove_from_this_list:
                    for s in search_this_list:
                        if r != s:
                            temp.append(r)
            else:
                temp = remove_from_this_list

            return temp


        # converts a python dictionary to a list
    def convertDictToList(dict):
            temp = []
            if dict is not None:
                for key, value in dict.items():
                    temp.append(key)
            return temp


    def removeValuesFromList(values_list, main_list):
            temp = []
            if values_list is not None and main_list is not None:
                for m in main_list:
                    add = True
                    for v in values_list:
                        if m == v:
                            add = False
                            break
                    if add:
                        temp.append(m)
            else:
                temp = main_list
            return temp


    def removeValueFromList(value, list):
            temp = []
            if list is not None:
                for li in list:
                    if li != value:
                        temp.append(li)
            else:
                temp = list
            return temp


    def compareLists(list1, list2):
        # returns true if there are matching values in the 2 lists
        if list1 is not None and list2 is not None:
            for a in list1:
                for b in list2:
                    if a == b:
                        return True
        return False

    def arrayContainsValue(array, value):
        if array is not None:
            for item in array:
                if item == value:
                    return True
        return False
