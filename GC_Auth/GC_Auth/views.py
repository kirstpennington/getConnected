from django.http import HttpResponseRedirect
from django.shortcuts import render
import pyrebase
from django.contrib import auth

config = {

    'apiKey': "AIzaSyCW2DTUu_qEhCG9xpj5gGkG2_QC_CmsGQE",
    'authDomain': "getconnected-9dac0.firebaseapp.com",
    'databaseURL': "https://getconnected-9dac0.firebaseio.com",
    'projectId': "getconnected-9dac0",
    'storageBucket': "getconnected-9dac0.appspot.com",
    'messagingSenderId': "144309081376"
}

# these objects only store info that the user updates manually-info that is not constantly being updates
# class with user profile info
class User:
    def __init__(self, name, bio, numConn, numForum, numCourse, em, pa, country, profPic, bPic, id, courseList, forumList, topics):
        self.username = name
        self.bio = bio
        self.numConnections = numConn
        self.numForums = numForum
        self.numCourses = numCourse
        self.email = em
        self.password = pa
        self.country = country
        self.profilePic = profPic
        self.backgroundPic = bPic
        self.uid = id
        self.coursesInfoList = courseList
        self.forumsInfoList = forumList
        self.topicsList = topics


# class with user privacy info
class Privacy:
    def __init__(self, bio, connections, country, name, pic, c, f):
        self.bio = bio
        self.connections = connections
        self.country = country
        self.name = name
        self.pic = pic
        self.course = c
        self.forums = f


# global variables
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

r = ""  # store initial user request for authentication
u = ""  # store user variable for Firebase authentication

the_user = ""       # object to store user information
user_privacy = ""   # object to store user privacy information




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
    if getBackgroundPic(request, user['localId']) == "":
        updateBackgroundPic(user,"https://cdn.shopify.com/s/files/1/2656/8500/products/galerie-wallpapers-unplugged-textured-plain-grey-wallpaper-2035691716651_1024x.jpg?v=1522251583")

    if getProfilePic(request, user['localId']) == "":
        updateProfilePic(user,  "https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg" )

    global the_user     # create the_user object to store user profile data
    the_user = User(getUsername(user['localId']),
                    getBio(request, user['localId']),
                    getNumConnecions(request, user['localId']),
                    getNumForums(request, user['localId']),
                    getNumCourses(request, user['localId']),
                    email,
                    password,
                    getCountry(user['localId']),
                    getProfilePic(request, user['localId']),
                    getBackgroundPic(request, user['localId']),
                    user['localId'],
                    getCoursesInfoList(getCoursesList(user['localId'])),
                    getForumsInfoList(getForumssList(user['localId'])),
                    getUserTopicsList(user['localId'])
                    )

    global user_privacy # create user_privacy object to store user privacy data
    user_privacy = Privacy(getBioPrivacy(user['localId']),
                           getConnectionPrivacy(user['localId']),
                           getCountryPrivacy(user['localId']),
                           getNamePrivacy(user['localId']),
                           getPicPrivacy(user['localId']),
                           getCoursesPrivacy(user['localId']),
                           getForumsPrivacy(user['localId']))

    # navigate to the user profile page and
    return render(request, "UserProfile.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic': the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic,
                                                'courses_list': the_user.coursesInfoList,
                                                'forums_list': the_user.forumsInfoList,
                                                'connections_suggestions_list': getConnectionsSuggestions(user['localId'], 1),
                                                'forums_suggestions_list': getForumSuggestions(user['localId'], 1)
                                                })
# ToDo: separate these into individual data items for the UI, only 3 of each required
# ToDo: include individual suggestions as well - 2 of each


def logout(request):
    auth.logout(request)
    return render(request, 'LogIn.html')







# READ methods

def getTrendingForums(request):
    all_forums_ids = database.child("Forums").shallow().get().val()                     # get a list of all forum id's
    # ToDo: find a way to calcuate trending forums

    for forum_id in all_forums_ids:
        private = database.child("Forums").child(forum_id).child("Private").get().val()
        # if private == "False" or private == "false":                                    # only consider the public forums


def getPrivacySettings(request):
    # Name of html file to be changed
        return render(request, "PrivacySettings.html", {'bioPrivacy': user_privacy.bio,
                                                        'connectionPrivacy': user_privacy.connections,
                                                        'countryPrivacy': user_privacy.country,
                                                        'namePrivacy': user_privacy.name,
                                                        'pPicPrivacy': user_privacy.pic,
                                                        })


# individual get methods - these methods are only used when the user signs in. Otherwise, data is taken from the the_user object

def getUsername(uid):
    return database.child('Users').child(uid).child('Name').get().val()


def getBio(request, uid):
    return database.child('Users').child(uid).child('Bio').get().val()


def getCountry(uid):
    return database.child('Users').child(uid).child('Country').get().val()


def getNumConnecions(request, uid):
    return database.child('Users').child(uid).child('numConnections').get().val()


def getNumForums(request, uid):
    return int(database.child('Users').child(uid).child('numForums').get().val())

def getNumCourses(request, uid):
    return int(database.child('Users').child(uid).child('numCourses').get().val())


def getProfilePic(request, user):
    return database.child('Users').child(user['localId']).child('ProfilePic').get().val()


def getProfilePic(request, uid):
    return database.child('Users').child(uid).child('ProfilePic').get().val()


def getBackgroundPic(request, uid):
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

# for filling the Courses blocks
def getCoursesList(uid):
    # get list of courses IDs that a user takes
    # code from : https://www.hackanons.com/2018/05/python-django-with-google-firebase_31.html
    course_ids = database.child('Users').child(uid).child('Courses').shallow().get().val()
    course_id_list = []     # stores list of course ids for the user
    for i in course_ids:
        course_id_list.append(i)
    return course_id_list


def getConnectionsInfoList(connections_id_list):
    names = []
    countries = []
    pictures = []

    for id in connections_id_list:
        if getNamePrivacy(id) == "False":  # checks the user's privacy settings before displaying it in the suggestion
            names.append(getUsername(id))
        else:
            names.append("User's Name Private")

        if getCountryPrivacy(
                id) == "False":  # checks the user's privacy settings before displaying it in the suggestion
            countries.append(getCountry(id))
        else:
            countries.append("User's Country Private")

        if getPicPrivacy(id) == "False":  # checks the user's privacy settings before displaying it in the suggestion
            pictures.append(getProfilePic("", id))
        else:
            pictures.append("https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg")

    return zip(names, countries, pictures)




def getCoursesInfoList(courses_id_list):
    # get data from each course for the user and add them to separate arrays
    course_names = []
    course_pictures = []
    course_recommendations = []
    course_urls = []
    course_uni_pics = []

    for id in courses_id_list:
        course_names.append(getCourseName(id))
        course_pictures.append(getCoursePicture(id))
        course_recommendations.append(getCourseRecommended(id))
        course_urls.append(getCourseURL(id))
        course_uni_pics.append(getCourseUniPic(id))

    # return a combination of all lists
    combined_list = zip(course_names, course_pictures, course_recommendations, course_urls, course_uni_pics)
    return combined_list


# Individual Course Data retrieval


def getCourseName(course_id):
    return database.child("Courses").child(course_id).child("CourseName").get().val()


def getCoursePicture(course_id):
    return database.child("Courses").child(course_id).child("Picture").get().val()


def getCourseUniversity(course_id):
    return database.child("Courses").child(course_id).child("University").get().val()


def getCourseUniPic(course_id):
    return database.child("Courses").child(course_id).child("UniPic").get().val()


def getCourseRecommended(course_id):
    # determines whether the course is recommended based on the number of hearts or recommednations
    # can change parameters if required
    num_rec = int(database.child("Courses").child(course_id).child("NumRecommendations").get().val())

    if num_rec < 200:
        return ""

    if num_rec>= 200 and num_rec<500:
        return "Recommended"

    if num_rec >= 500:
        return "Highly Recommended"



def getCourseURL(course_id):
    return database.child("Courses").child(course_id).child("CourseURL").get().val()
# ToDo: does not appear when navigating back to the user profile page

# for filling the Courses blocks
def getForumssList(uid):
    # get list of forum IDs that a user takes
    # code from : https://www.hackanons.com/2018/05/python-django-with-google-firebase_31.html
    forum_ids = database.child('Users').child(uid).child('ForumVisits').shallow().get().val()
    forum_id_list = []     # stores list of course ids for the user
    for i in forum_ids:
        forum_id_list.append(i)
    return forum_id_list


def getForumsInfoList(forums_id_list):
    # get data from each course for the user and add them to separate arrays
    forum_names = []
    forum_pics = []
    forum_num_participants = []
    forum_creators = []
    forum_topics = []

    for id in forums_id_list:
        forum_names.append(getForumName(id))
        forum_pics.append(getForumPic(id))
        forum_pics.append(getForumNumParticipants(id))
        forum_pics.append(getForumCreator(id))
        forum_pics.append(getForumTopicsString(id))

    # return a combination of all lists
    combined_forums_list = zip(forum_names, forum_pics, forum_num_participants, forum_creators, forum_topics)
    return combined_forums_list

# ToDo: this function is not working at all
# Individual Forum Data retrieval
def getForumName(forum_id):
    return database.child("Forums").child(forum_id).child("Name").get().val()


def getForumPic(forum_id):
    return database.child("Forums").child(forum_id).child("ForumPic").get().val()


def getForumNumParticipants(forum_id):
    return database.child("Forums").child(forum_id).child("NumParticipants").get().val()


def getForumCreator(forum_id):
    return database.child("Forums").child(forum_id).child("Creator").get().val()


def getForumTopicsString(forum_id):
    # gets all topics and puts them into one string
    topics = database.child("Forums").child(forum_id).child("TopicTags").shallow().get().val()
    topics_string = ""
    for topic in topics:
        topics_string = topics_string + ", " + topic

    return topics_string



# Suggestions Carousel methods
# ToDo: suggestions carousel (user profile)

def getForumSuggestions(uid, num_returns):
    # returns a combined list of forum information with the same topics as this user's interests
    results_count = 0                                                                               # how many results were found thus far
    results = []
    all_forums_list = database.child("Forums").shallow().get().val()                                # list of this user's interests

    for compare_forum_id in all_forums_list:
        if results_count == num_returns:                                                            # if we have the requested number of ids, stop searching
            break
        else:
                                                                                                    # get the topics of the user we are currently comparing this user with
            private = database.child("Forums").child(compare_forum_id).child("Private").get().val()
            if private == "False" or private == "false":                                            # the forum must be private for it to be suggested to other users
                compare_forum_topics = database.child("Forums").child(compare_forum_id).child("TopicTags").shallow().get().val()
                if compareLists(compare_forum_topics, the_user.topicsList):                         # if we find a match, add it to the list of results
                    results.append(compare_forum_id)
                    results_count += 1

                                                                                                    # get list of this user's joined forums - includes forums they created
    all_user_forums = database.child("Users").child(uid).child("ForumsJoined").shallow().get().val()

                                                                                                    # remove users that are already connections and return this updated list
    try:
        final_results = removeValuesFromList(results, all_user_forums)
    except:
                                                                                                    # if all_user_forums is empty
        final_results = results

    return getForumsInfoList(final_results)


def getCourseSuggestions(uid, num_returns):
    # returns a combines list of courses that match the user's interests
    results_count = 0  # how many results were found thus far
    results = []

    all_courses_list = database.child("Courses").shallow().get().val()               # list of all courses in the db - only their id's
    all_user_courses = database.child("Users").child(uid).child("Courses").shallow().get().val()    # list of all courses that this user has done
    try:
        courses_list = removeValuesFromList(all_courses_list, all_user_courses)                                # remove the courses that the user has already done from the list of all courses
    except:
        courses_list = all_courses_list                                                             # except will be reached if user has no courses

    for compare_course_id in courses_list:                                                          # loop through each course in the list
        if results_count == num_returns:                                                            # if we have the requested number of ids, stop searching
            break
        else:                                                                                       # get the list of topics for each course
            compare_courses_topics = database.child("Courses").child(compare_course_id).child("Topic").shallow().get().val()
            if compareLists(compare_courses_topics, the_user.topicsList):                           # if there are matching topics between the user and the course
                results.append(compare_course_id)                                                       # add the course to the list of suggestions
                results_count += 1                                                                      # increment number fo results by 1

    return getCoursesInfoList(results)


def getConnectionsSuggestions(uid, num_returns):
    # returns a combined list of user information with the same interests as this user
    results_count = 0                                                                               # how many results were found thus far
    results = []

    all_users_list_1 = database.child("Users").shallow().get().val()                                # list of all users in the system
    all_users_list = removeValueFromList(uid, all_users_list_1)                                     # remove this user from the list of all users
    for compare_user_id in all_users_list:
        if results_count == num_returns:                                                            # if we have the requested number of ids, stop searching
            break
        else:
                                                                                                    # get the topics of the user we are currently comparing this user wih
            compare_user_interests = database.child("Users").child(compare_user_id).child("Topics").shallow().get().val()
            if compareLists(compare_user_interests, the_user.topicsList):                           # if we find a match, add it to the list of results
                results.append(compare_user_id)
                results_count += 1

    user_connections_list = database.child("Users").child('Connections').shallow().get().val()      # get list of this user connections

    try:                                                                                            # remove users that are already connections and return this updated list
        final_results = removeValuesFromList(results, user_connections_list)
    except:
        final_results = results

<<<<<<< Updated upstream
    return getConnectionsInfoList(final_results)
=======
    # navigate to the user profile page and
    return render(request, "User_Profile_Page.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic':the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic})
>>>>>>> Stashed changes


# supporting methods for finding suggestions
def removeCommons(remove_from_this_list, search_this_list):
    # removes the common values between the 2 lists from the first list
    temp = []    # dummy variable where items from the list will be removed
    for r in remove_from_this_list:
        for s in search_this_list:
            if r != s:
                temp.append(r)
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
    for l in list:
        if l != value:
            temp.append(l)
    return temp


def compareLists(list1, list2):
    # returns true if there are matching values in the 2 lists
    for a in list1:
        for b in list2:
            if a == b:
                return True
    return False


def getUserTopicsList(uid):
    # get this user's interests/topics in a list
    return database.child("Users").child(uid).child("Topics").shallow().get().val()

# ToDo: courses page
# ToDo: forums page

# ToDo: trending forums carousel (launch page)


# UPDATE Methods

def updateProfile(request):

    if request.method == "POST":
        # get data from UI using POST method
        name = request.POST.get("name")
        bio = request.POST.get("bio")
        country = request.POST.get("country")
        email = request.POST.get("email")


    # call each method to update elements of the profile in the db
    updateUsername(u, name)
    updateBio(u, bio)
    updateCountry(u, country)
    updateEmail(u, email)

    # edit return render to show the new data
<<<<<<< Updated upstream
    return render(request, "UserProfile.html", {'n': name,
                                                'email': email,
=======
    return render(request, "User_Profile_Page.html", {'n': name,
>>>>>>> Stashed changes
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
        coursesPrivacy = request.POST.get("coursesPrivacy")
        forumsPrivacy = request.POST.get("forumsPrivacy")

    # call each method to update elements of the profile in the db
    updateBioPrivacy(u, bioPrivacy)
    updateConnectionPrivacy(u, connectionPrivacy)
    updateCountryPrivacy(u, countryPrivacy)
    updateNamePrivacy(u, namePrivacy)
    updatePicPrivacy(u, pPicPrivacy)
    updateCoursesPrivacy(u, coursesPrivacy)
    updateForumsPrivacy(u, forumsPrivacy)


    # edit return render to show the new data
    return render(request, "User_Profile_Page.html", {'bioPrivacy': bioPrivacy,
                                                'connectionPrivacy': connectionPrivacy,
                                                'countryPrivacy': countryPrivacy,
                                                'namePrivacy': namePrivacy,
                                                'pPicPrivacy': pPicPrivacy,
                                                'coursesPrivacy': coursesPrivacy,
                                                'forumsPrivacy': forumsPrivacy
                                                })
    # individual update methods


def updateUsername(user, name):
    database.child("Users").child(user['localId']).update({"Name": name})   # update element in the database
    try:  # try except for purpose of unit tests
        global the_user
        the_user.username = name        # update element in the local object
    except:
        return ""

def updateEmail(user, e):
  # insert code to update email address (optional)
    try:
        global the_user
        the_user.email = e
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
    return render(request, "User_Profile_Page.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic': the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic,
                                                'courses_list': the_user.coursesInfoList})

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
    return render(request, "User_Profile_Page.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic': the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic,
                                                'courses_list': the_user.coursesInfoList})


def updateBackgroundPic(user, bPic):
    database.child("Users").child(user['localId']).update({"BackgroundPic": bPic})
    try: # try except for purpose of unit tests
        global the_user
        the_user.backgroundPic = bPic
    except:
        return ""


def deleteProfilePic(request):
        updateProfilePic(u, "https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg")


def deleteBackgroundPic(request):
    updateBackgroundPic(u, "https://cdn.shopify.com/s/files/1/2656/8500/products/galerie-wallpapers-unplugged-textured-plain-grey-wallpaper-2035691716651_1024x.jpg?v=1522251583")


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


def updateCoursesPrivacy(user, coursesPrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"CoursesPrivacy": coursesPrivacy})
    try:  # try except for purpose of unit tests
        global user_privacy
        user_privacy.courses = coursesPrivacy
    except:
        return ""


def updateForumsPrivacy(user, forumsPrivacy):
    database.child("Users").child(user['localId']).child("UserPrivacy").update({"ForumsPrivacy": forumsPrivacy})
    try:  # try except for purpose of unit tests
        global user_privacy
        user_privacy.forums = forumsPrivacy
    except:
        return ""


# ToDo: code to add ratings to courses


# Navigation Methods

def home(request):
     return render(request, "User_Profile_Page.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic': the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic,
                                                'courses_list': the_user.coursesInfoList,
                                                'forums_list': the_user.forumsInfoList,
                                                'connections_suggestions_list': getConnectionsSuggestions(the_user.uid, 1),
                                                'forums_suggestions_list': getForumSuggestions(the_user.uid, 1)
                                                 })


def networks(request):
    return render(request, 'MyNetwork.html')


def forums(request):
    return render(request, 'Forums.html', {'forums_list': the_user.forumsInfoList,
                                           'suggested_forums_list': getForumSuggestions(the_user.uid, 3)})


def courses(request):
    return render(request, 'Courses.html', {'courses_list': the_user.coursesInfoList,
                                            'suggested_courses_list': getCourseSuggestions(the_user.uid, 3)})


def connections(request):
    return render(request, 'Connections.html', {'connections_list': getConnectionsInfoList(getUserConnectionsList(the_user.uid)),
                                                'suggested_connections_list': getConnectionsSuggestions(the_user, 3)})


def userprofile(request):
    return render(request, "User_Profile_Page.html", {"e": the_user.email,
                                                'n': the_user.username,
                                                'bio': the_user.bio,
                                                'email': the_user.email,
                                                'country': the_user.country,
                                                'numConnections': the_user.numConnections,
                                                'numForums': the_user.numForums,
                                                'ProfilePic': the_user.profilePic,
                                                'backgroundPic': the_user.backgroundPic,
                                                'courses_list': the_user.coursesInfoList,
                                                'forums_list': the_user.forumsInfoList,
                                                'connections_suggestions_list': getConnectionsSuggestions(the_user.uid,1),
                                                'forums_suggestions_list': getForumSuggestions(the_user.uid, 1)
                                                })


def goSettings(request):
    return render(request, "Setttings.html")


def goBadges(request):
    # user authentication with Firebase
    return render(request, "badgesStart.html", {
        'n': the_user.username,
        'numConnections': the_user.numConnections,
        'numForums': the_user.numForums,
        'numCourses': the_user.numCourses,
        'biopriv': user_privacy.bio,

    })


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





