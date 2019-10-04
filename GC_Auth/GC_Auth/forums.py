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


class forum_methods:

# GET Methods
    def getForumName(forum_id):
        return database.child("Forums").child(forum_id).child("Name").get().val()

    def getForumPic(forum_id):
        return database.child("Forums").child(forum_id).child("ForumPic").get().val()

    def getForumNumParticipants(forum_id):
        temp = database.child('Forums').child(forum_id).child('Participants').shallow().get().val()

        if temp is None:
            return 0
        else:
            return len(temp)

    def getForumCreator(forum_id):
        return database.child("Forums").child(forum_id).child(
            "Creator").get().val()  # get the user id of the forum creator

    def getForumEnabled(forum_id):
        return database.child("Forums").child(forum_id).child("Enabled").get().val()

    def getForumDescription(forum_id):
        return database.child("Forums").child(forum_id).child("Description").get().val()

    def getForumPrivate(forum_id):
        return database.child("Forums").child(forum_id).child("Private").get().val()

    def getForumTopicsString(forum_id):
        # gets all topics and puts them into one string
        topics = database.child("Forums").child(forum_id).child("TopicTags").shallow().get().val()
        if topics is None:
            return "No Topics"
        else:
            for topic in topics:
                return "| " + topic + " |"              # return the first topic in the list


    def getForumTopicsList(forum_id):
        return database.child("Forums").child(forum_id).child("TopicTags").shallow().get().val()

    def getMessageText(forum_id, mess_id):
        return database.child("Forums").child(forum_id).child("Messages").child(mess_id).child("text").get().val()


    def getMessageSenderPic(forum_id, mess_id):
        return database.child("Forums").child(forum_id).child("Messages").child(mess_id).child("sender_profilePic").get().val()

    def getMessageSenderName(forum_id, mess_id):
        return database.child("Forums").child(forum_id).child("Messages").child(mess_id).child("sender_name").get().val()

    def getMessageSenderID(forum_id, mess_id):
        return database.child("Forums").child(forum_id).child("Messages").child(mess_id).child("sender").get().val()

    def getMessageNumComments(forum_id, mess_id):
        return database.child("Forums").child(forum_id).child("Messages").child(mess_id).child("comments_num").get().val()

    def getMessageNumLikes(forum_id, mess_id):
        return database.child("Forums").child(forum_id).child("Messages").child(mess_id).child("likes").get().val()

    def getMessageCommentIDs(forum_id, mess_id):
        return database.child("Forums").child(forum_id).child("Messages").child(mess_id).child("comments").shallow().get().val()

    def getMessageLikeIDs(forum_id, mess_id):
        return database.child("Forums").child(forum_id).child("Messages").child(mess_id).child("likes_ids").shallow().get().val()

    # Suggestions Carousel methods

    def getForumMessages(forum_id):
        mess_ids = database.child("Forums").child(forum_id).child("Messages").shallow().get().val()           # get all message ids
        texts = []
        sender_pic = []
        sender_name = []
        sender_id = []
        num_comments = []
        num_likes = []
        comment_ids = []
        like_ids = []

        if mess_ids is not None:
            for mess_id in mess_ids:
                texts.append(forum_methods.getMessageText(forum_id, mess_id))
                sender_pic.append(forum_methods.getMessageSenderPic(forum_id, mess_id))
                sender_name.append(forum_methods.getMessageSenderName(forum_id, mess_id))
                sender_id.append(forum_methods.getMessageSenderID(forum_id, mess_id))
                num_comments.append(forum_methods.getMessageNumComments(forum_id, mess_id))
                num_likes.append(forum_methods.getMessageNumLikes(forum_id, mess_id))
                comment_ids.append(forum_methods.getMessageCommentIDs(forum_id, mess_id))
                like_ids.append(forum_methods.getMessageLikeIDs(forum_id, mess_id))

        combined_list =  zip(mess_ids, texts, sender_pic, sender_name, sender_id, num_comments, num_likes, comment_ids, like_ids)
        return combined_list

    def getUsername(uid):
        return database.child('Users').child(uid).child('Name').get().val()

    def getForumsInfoList(forums_id_list):
        # get data from each course for the user and add them to separate arrays
        forum_names = []
        forum_pics = []
        forum_num_participants = []
        forum_creators = []
        forum_topics = []
        forum_descriptions = []
        forum_ids = []

        if forums_id_list is not None:
            for id in forums_id_list:
                forum_names.append(forum_methods.getForumName(id))
                forum_pics.append(forum_methods.getForumPic(id))
                forum_num_participants.append(forum_methods.getForumNumParticipants(id))
                forum_creators.append(forum_methods.getUsername(forum_methods.getForumCreator(id)))
                forum_topics.append(forum_methods.getForumTopicsString(id))
                forum_descriptions.append(forum_methods.getForumDescription(id))
                forum_ids.append(id)

        # return a combination of all lists
        combined_forums_list = zip(forum_names, forum_pics, forum_num_participants, forum_creators, forum_topics,
                                   forum_descriptions, forum_ids)
        return combined_forums_list


    def getAllForumsList(uid):
        all_forums = database.child("Forums").shallow().get().val()
        if all_forums is None:      # make sure no error is returned if there are no forums in the DB
            return []
        else:               # remove the forums I've joined from the allforums list
            forums_joined = database.child('Users').child(uid).child('ForumsJoined').shallow().get().val()
            return forum_methods.removeValuesFromList(forums_joined, all_forums)

    def getForumSuggestions(uid, num_returns, the_user):
        # returns a combined list of forum information with the same topics as this user's interests
        results_count = 0                                                       # how many results were found thus far
        results = []
        all_forums_list = database.child("Forums").shallow().get().val()        # list of this user's interests
        # get list of this user's joined forums - includes forums they created
        all_user_forums = database.child("Users").child(uid).child("ForumsJoined").shallow().get().val()

        for compare_forum_id in all_forums_list:

            if results_count == num_returns:                                    # if we have the requested number of ids, stop searching
                break
            else:
                if forum_methods.arrayContainsValue(all_user_forums, compare_forum_id) == False:        # if the user has not already joined this forum
                    forum_enabled = database.child("Forums").child(compare_forum_id).child("Enabled").shallow().get().val()

                    if forum_enabled == 'true' or forum_enabled == True:                                     # check that the forum is enabled before suggesting it
                        compare_forum_topics = database.child("Forums").child(compare_forum_id).child(
                                "TopicTags").shallow().get().val()
                        compare_user_topics = database.child("Users").child(uid).child("Topics").shallow().get().val()

                        if forum_methods.compareLists(compare_forum_topics, compare_user_topics):                   # if we find a match, add it to the list of results
                            results.append(compare_forum_id)
                            results_count += 1

        if results is None:
            return []
        else:
            return results


    def getTrendingForums(self):
        # list of the top 3 public forums with the most participants
        temp = database.child("Forums").shallow().get().val()                   # get a list of all forum id's
        all_forums_ids = []                                                     # remove all private forums
        for forum_id in temp:
            private = database.child("Forums").child(forum_id).child("Private").get().val()
            if private != "True" or private != "true":                          # only consider public forums
                all_forums_ids.append(forum_id)

        top_forum_ids = []                                                      # stores the forum with the most number of participants

        if len(all_forums_ids) >= 3:
            top_forum_ids.append(all_forums_ids[0])
            top_forum_ids.append(all_forums_ids[1])
            top_forum_ids.append(all_forums_ids[2])

            count_skip = 0                                                      # skip the first 3 values because they're already in the top forums list
            for forum_id in all_forums_ids:
                if count_skip >= 3:
                    for i in range(len(top_forum_ids)):
                        participants_forum = forum_methods.getForumNumParticipants(forum_id)
                        participants_next = forum_methods.getForumNumParticipants(top_forum_ids[i])
                        if participants_forum is None:
                            participants_forum = 0
                        if participants_next is None:
                            participants_next = 0
                        if participants_forum > participants_next:                              # compare which forum has more participants
                            top_forum_ids[i] = forum_id
                            break
                count_skip += 1
        else:
            top_forum_ids = all_forums_ids

        return forum_methods.getForumsInfoList(top_forum_ids)


    # supporting methods for finding suggestions
    def removeCommons(remove_from_this_list, search_this_list):
        # removes the common values between the 2 lists from the first list
        temp = []    # dummy variable where items from the list will be removed

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

# UPDATE Methods