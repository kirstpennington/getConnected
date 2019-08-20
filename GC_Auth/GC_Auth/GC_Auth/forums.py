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
        return database.child("Forums").child(forum_id).child("NumParticipants").get().val()

    def getForumCreator(forum_id):
        user_id = database.child("Forums").child(forum_id).child(
            "Creator").get().val()  # get the user id of the forum creator
        return database.child("Users").child(user_id).child(
            "Name").get().val()  # get the user's name using the user's id

    def getForumDescription(forum_id):
        return database.child("Forums").child(forum_id).child("Description").get().val()


    def getForumTopicsString(forum_id):
        # gets all topics and puts them into one string
        topics = database.child("Forums").child(forum_id).child("TopicTags").shallow().get().val()
        topics_string = ""

        for topic in topics:
            topics_string = topics_string + " | " + topic

        topics_string += " | "
        return topics_string

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
        print('forum_id',forum_id)
        mess_ids = database.child("Forums").child(forum_id).child("Messages").shallow().get().val()           # get all message ids
        texts = []
        sender_pic = []
        sender_name = []
        sender_id = []
        num_comments = []
        num_likes = []
        comment_ids = []
        like_ids = []

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

    def getForumsInfoList(forums_id_list):
        # get data from each course for the user and add them to separate arrays
        forum_names = []
        forum_pics = []
        forum_num_participants = []
        forum_creators = []
        forum_topics = []
        forum_descriptions = []
        forum_ids = []

        for id in forums_id_list:
            forum_names.append(forum_methods.getForumName(id))
            forum_pics.append(forum_methods.getForumPic(id))
            forum_num_participants.append(forum_methods.getForumNumParticipants(id))
            forum_creators.append(forum_methods.getForumCreator(id))
            forum_topics.append(forum_methods.getForumTopicsString(id))
            forum_descriptions.append(forum_methods.getForumDescription(id))
            forum_ids.append(id)

        # return a combination of all lists
        combined_forums_list = zip(forum_names, forum_pics, forum_num_participants, forum_creators, forum_topics,
                                   forum_descriptions, forum_ids)
        return combined_forums_list


    def getAllForumsList(uid):
        return database.child("Forums").shallow().get().val()

    def getForumSuggestions(uid, num_returns, the_user):
        # returns a combined list of forum information with the same topics as this user's interests
        results_count = 0  # how many results were found thus far
        results = []
        all_forums_list = database.child("Forums").shallow().get().val()  # list of this user's interests

        for compare_forum_id in all_forums_list:
            if results_count == num_returns:  # if we have the requested number of ids, stop searching
                break
            else:
                private = database.child("Forums").child(compare_forum_id).child("Private").get().val()
                if private != "True" or private != "true":  # the forum must be private for it to be suggested to other users
                    compare_forum_topics = database.child("Forums").child(compare_forum_id).child(
                        "TopicTags").shallow().get().val()
                    if forum_methods.compareLists(compare_forum_topics,
                                    the_user.topicsList):  # if we find a match, add it to the list of results
                        results.append(compare_forum_id)
                        results_count += 1

                        # get list of this user's joined forums - includes forums they created
        all_user_forums = database.child("Users").child(uid).child("ForumsJoined").shallow().get().val()
        try:
            final_results = forum_methods.removeValuesFromList(all_user_forums,
                                                 results)  # remove users that are already connections and return this updated list
        except:
            final_results = results

        return final_results


    def getTrendingForums(self):
        # list of the top 3 public forums with the most participants
        temp = database.child("Forums").shallow().get().val()  # get a list of all forum id's
        all_forums_ids = []  # remove all private forums
        for forum_id in temp:
            private = database.child("Forums").child(forum_id).child("Private").get().val()
            if private != "True" or private != "true":  # only consider public forums
                all_forums_ids.append(forum_id)

        top_forum_ids = []  # stores the forum with the most number of participants

        if len(all_forums_ids) >= 3:
            top_forum_ids.append(all_forums_ids[0])
            top_forum_ids.append(all_forums_ids[1])
            top_forum_ids.append(all_forums_ids[2])

            count_skip = 0  # skip the first 3 values because they're already in the top forums list
            for forum_id in all_forums_ids:
                if count_skip >= 3:
                    for i in range(len(top_forum_ids)):
                        if forum_methods.getForumNumParticipants(forum_id) > forum_methods.getForumNumParticipants(
                                top_forum_ids[i]):  # compare which forum has more participants
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


# UPDATE Methods