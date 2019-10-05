from django.http import HttpResponseRedirect
from django.shortcuts import render
import pyrebase
from django.contrib import auth
from GC_Auth.Privacy import Privacy
from GC_Auth.User import User
from GC_Auth.courses import course_methods
from GC_Auth.forums import forum_methods
from GC_Auth.users import user_methods
from GC_Auth.connections import connection_methods

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

r = ""  # store initial user request for authentication
u = ""  # store user variable for Firebase authentication

the_user = ""  # object to store user information
user_privacy = ""  # object to store user privacy information

email = ""


# LOGIN methods

short_connections_suggestions = ""  # stored all suggested forums, courses and connections for faster loading times
short_forum_suggestions = ""
short_course_suggestions = ""


# LOGIN methods

def LogIn(request):
    forum_names, forum_pics, forum_num_participants, forum_creators, forum_topics, forum_descriptions, forum_ids = zip(
        *forum_methods.getTrendingForums(""))  # unzip all elements of each trending forum

    if len(forum_names) == 0:
        return render(request, "LogIn.html", {'show_forum_1': 'hidden',
                                              'show_forum_2': 'hidden',
                                              'show_forum_3': 'hidden'})
    if len(forum_names) == 1:
        return render(request, "LogIn.html", {'show_forum_1': 'visible',
                                              'forum_1_pic': forum_pics[0],
                                              'forum_1_participants': forum_num_participants[0],
                                              'forum_1_name': forum_names[0],
                                              'forum_1_description': forum_descriptions[0],
                                              'show_forum_2': 'hidden',
                                              'show_forum_3': 'hidden'})
    if len(forum_names) == 2:
        return render(request, "LogIn.html", {'show_forum_1': 'visible',
                                              'forum_1_pic': forum_pics[0],
                                              'forum_1_participants': forum_num_participants[0],
                                              'forum_1_name': forum_names[0],
                                              'forum_1_description': forum_descriptions[0],
                                              'show_forum_2': 'visible',
                                              'forum_2_pic': forum_pics[1],
                                              'forum_2_participants': forum_num_participants[1],
                                              'forum_2_name': forum_names[1],
                                              'forum_2_description': forum_descriptions[1],
                                              'show_forum_3': 'hidden'})

    return render(request, "LogIn.html", {'show_forum_1': 'visible',
                                          'forum_1_pic': forum_pics[0],
                                          'forum_1_participants': forum_num_participants[0],
                                          'forum_1_name': forum_names[0],
                                          'forum_1_description': forum_descriptions[0],
                                          'show_forum_2': 'visible',
                                          'forum_2_pic': forum_pics[1],
                                          'forum_2_participants': forum_num_participants[1],
                                          'forum_2_name': forum_names[1],
                                          'forum_2_description': forum_descriptions[1],
                                          'show_forum_3': 'visible',
                                          'forum_3_pic': forum_pics[2],
                                          'forum_3_participants': forum_num_participants[2],
                                          'forum_3_name': forum_names[2],
                                          'forum_3_description': forum_descriptions[2]
                                          })



def passwordReset(request):
    # ... your python code/script
    return render(request, "passwordReset.html")


def postsign(request):
    # user authentication with Firebase
    global r
    r = request

    global email
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

    global the_user  # create the_user object to store user profile data

    # if the user image or background is blank, set it to a default value
    if user_methods.getBackgroundPic(user['localId']) == "":
        user_methods.updateBackgroundPic(user['localId'],
                                         "https://cdn.shopify.com/s/files/1/2656/8500/products/galerie-wallpapers-unplugged-textured-plain-grey-wallpaper-2035691716651_1024x.jpg?v=1522251583")
        the_user.backgroundPic = "https://cdn.shopify.com/s/files/1/2656/8500/products/galerie-wallpapers-unplugged-textured-plain-grey-wallpaper-2035691716651_1024x.jpg?v=1522251583"

    if user_methods.getProfilePic(user['localId']) == "":
        user_methods.updateProfilePic(user['localId'],
                                      "https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg")
        the_user.profilePic = "https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg"

    user_methods.updateAccountEnabled(user['localId'], "true")

    the_user = User(user_methods.getUsername(user['localId']),
                    user_methods.getBio(user['localId']),
                    user_methods.getNumConnecions(user['localId']),
                    user_methods.getNumForums(user['localId']),
                    user_methods.getNumCourses(user['localId']),
                    email,
                    password,
                    user_methods.getCountry(user['localId']),
                    user_methods.getProfilePic(user['localId']),
                    user_methods.getBackgroundPic(user['localId']),
                    user['localId'],
                    user_methods.getCoursesList(user['localId']),
                    user_methods.getForumssList(user['localId']),
                    user_methods.getUserConnectionsList(user['localId']),
                    user_methods.getUserTopicsList(user['localId']),
                    password
                    )

    global short_course_suggestions  # preload course suggestions
    short_course_suggestions = course_methods.getCourseSuggestions(user['localId'], 3, the_user)

    global user_privacy  # create user_privacy object to store user privacy data
    user_privacy = Privacy(user_methods.getBioPrivacy(user['localId']),
                           user_methods.getConnectionPrivacy(user['localId']),
                           user_methods.getCountryPrivacy(user['localId']),
                           user_methods.getNamePrivacy(user['localId']),
                           user_methods.getPicPrivacy(user['localId']),
                           user_methods.getCoursesPrivacy(user['localId']),
                           user_methods.getForumsPrivacy(user['localId']))

    return returnUserProfileCarousels(request)


def logout(request):
    auth.logout(request)
    # do all stuff in confirm dialogue
    forum_names, forum_pics, forum_num_participants, forum_creators, forum_topics, forum_descriptions, forum_ids = zip(
        *forum_methods.getTrendingForums(""))  # unzip all elements of each trending forum

    if len(forum_names) == 0:
        return render(request, "LogIn.html", {'show_forum_1': 'hidden',
                                              'show_forum_2': 'hidden',
                                              'show_forum_3': 'hidden'})
    if len(forum_names) == 1:
        return render(request, "LogIn.html", {'show_forum_1': 'visible',
                                              'forum_1_pic': forum_pics[0],
                                              'forum_1_participants': forum_num_participants[0],
                                              'forum_1_name': forum_names[0],
                                              'forum_1_description': forum_descriptions[0],
                                              'show_forum_2': 'hidden',
                                              'show_forum_3': 'hidden'})
    if len(forum_names) == 2:
        return render(request, "LogIn.html", {'show_forum_1': 'visible',
                                              'forum_1_pic': forum_pics[0],
                                              'forum_1_participants': forum_num_participants[0],
                                              'forum_1_name': forum_names[0],
                                              'forum_1_description': forum_descriptions[0],
                                              'show_forum_2': 'visible',
                                              'forum_2_pic': forum_pics[1],
                                              'forum_2_participants': forum_num_participants[1],
                                              'forum_2_name': forum_names[1],
                                              'forum_2_description': forum_descriptions[1],
                                              'show_forum_3': 'hidden'})

    return render(request, "LogIn.html", {'show_forum_1': 'visible',
                                          'forum_1_pic': forum_pics[0],
                                          'forum_1_participants': forum_num_participants[0],
                                          'forum_1_name': forum_names[0],
                                          'forum_1_description': forum_descriptions[0],
                                          'show_forum_2': 'visible',
                                          'forum_2_pic': forum_pics[1],
                                          'forum_2_participants': forum_num_participants[1],
                                          'forum_2_name': forum_names[1],
                                          'forum_2_description': forum_descriptions[1],
                                          'show_forum_3': 'visible',
                                          'forum_3_pic': forum_pics[2],
                                          'forum_3_participants': forum_num_participants[2],
                                          'forum_3_name': forum_names[2],
                                          'forum_3_description': forum_descriptions[2]
                                          })


def logoutDisableAccount(request):
    auth.logout(request)
    forum_names, forum_pics, forum_num_participants, forum_creators, forum_topics, forum_descriptions, forum_ids = zip(
        *forum_methods.getTrendingForums(""))  # unzip all elements of each trending forum

    if len(forum_names) == 0:
        return render(request, "LogIn.html", {'show_forum_1': 'hidden',
                                              'show_forum_2': 'hidden',
                                              'show_forum_3': 'hidden'})
    if len(forum_names) == 1:
        return render(request, "LogIn.html", {'show_forum_1': 'visible',
                                              'forum_1_pic': forum_pics[0],
                                              'forum_1_participants': forum_num_participants[0],
                                              'forum_1_name': forum_names[0],
                                              'forum_1_description': forum_descriptions[0],
                                              'show_forum_2': 'hidden',
                                              'show_forum_3': 'hidden'})
    if len(forum_names) == 2:
        return render(request, "LogIn.html", {'show_forum_1': 'visible',
                                              'forum_1_pic': forum_pics[0],
                                              'forum_1_participants': forum_num_participants[0],
                                              'forum_1_name': forum_names[0],
                                              'forum_1_description': forum_descriptions[0],
                                              'show_forum_2': 'visible',
                                              'forum_2_pic': forum_pics[1],
                                              'forum_2_participants': forum_num_participants[1],
                                              'forum_2_name': forum_names[1],
                                              'forum_2_description': forum_descriptions[1],
                                              'show_forum_3': 'hidden'})

    return render(request, "LogIn.html", {'show_forum_1': 'visible',
                                          'forum_1_pic': forum_pics[0],
                                          'forum_1_participants': forum_num_participants[0],
                                          'forum_1_name': forum_names[0],
                                          'forum_1_description': forum_descriptions[0],
                                          'show_forum_2': 'visible',
                                          'forum_2_pic': forum_pics[1],
                                          'forum_2_participants': forum_num_participants[1],
                                          'forum_2_name': forum_names[1],
                                          'forum_2_description': forum_descriptions[1],
                                          'show_forum_3': 'visible',
                                          'forum_3_pic': forum_pics[2],
                                          'forum_3_participants': forum_num_participants[2],
                                          'forum_3_name': forum_names[2],
                                          'forum_3_description': forum_descriptions[2]
                                          })


# Called to update Profile Page from Settings.html page - leads to User Profile page
def updateProfile(request):
    if "cancel" in request.POST:
        return returnUserProfileCarousels(request)

    if request.method == "POST":
        # get data from UI using POST method
        name = request.POST.get("firstname")
        bio = request.POST.get("bioGet")
        if bio == "":
            bio = "No Bio yet..."
        country = request.POST.get("country")
        email = request.POST.get("email")
        bioPrivacy = request.POST.get("bioPrivacyGet")
        connectionPrivacy = request.POST.get("connectionPrivacyGet")
        countryPrivacy = request.POST.get("countryPrivacyGet")
        namePrivacy = request.POST.get("namePrivacy")
        pPicPrivacy = request.POST.get("pPicPrivacy")
        coursesPrivacy = request.POST.get("coursesPrivacyGet")
        forumsPrivacy = request.POST.get("forumPrivacyGet")

        global the_user
        global user_privacy

        if the_user.username != name:  # check is there was a change made first
            user_methods.updateUsername(the_user.uid,
                                        name)  # call each method to update elements of the profile in the db
            the_user.username = name  # edit the contents of the the_user variable

        if the_user.bio != bio:
            user_methods.updateBio(the_user.uid, bio)
            the_user.bio = bio

        if the_user.country != country:
            user_methods.updateCountry(the_user.uid, country)
            the_user.country = country

        if user_privacy.bio != bioPrivacy:
            user_methods.updateBioPrivacy(the_user.uid, bioPrivacy)
            user_privacy.bio = bioPrivacy

        if user_privacy.connections != connectionPrivacy:
            user_methods.updateConnectionPrivacy(the_user.uid, connectionPrivacy)
            user_privacy.connections = connectionPrivacy

        if user_privacy.country != countryPrivacy:
            user_methods.updateCountryPrivacy(the_user.uid, countryPrivacy)
            user_privacy.country = countryPrivacy

        if user_privacy.name != namePrivacy:
            user_methods.updateNamePrivacy(the_user.uid, namePrivacy)
            user_privacy.name = namePrivacy

        if user_privacy.pic != pPicPrivacy:
            user_methods.updatePicPrivacy(the_user.uid, pPicPrivacy)
            user_privacy.pic = pPicPrivacy

        if user_privacy.courses != coursesPrivacy:
            user_methods.updateCoursesPrivacy(the_user.uid, coursesPrivacy)
            user_privacy.courses = coursesPrivacy

        if user_privacy.forums != forumsPrivacy:
            user_methods.updateForumsPrivacy(the_user.uid, forumsPrivacy)
            user_privacy.forums = forumsPrivacy

    # edit return render to show the new data
    return returnUserProfileCarousels(request)  # render user profile with updated data


# method for updating only the profile pic
def updateProfilePicRequest(request):
    global the_user
    if request.method == "POST":  # get data from UI
        """pic = request.FILES.get("files[]")
        
        storage.child("images/", the_user.uid).put(pic)"""
        storage = firebase.storage()
        url = storage.child(the_user.uid).get_url()

        """newPic = request.POST.get("url")                     # get data from UI using POST method
        print("!newPic", newPic)
        global the_user                                             # edit the object value for profile pic
        the_user.profilePic = newPic

        if user_methods.getUpdatedProfilePic(
                the_user.uid) != "yes":                             # tracks whether the user has updated their profile pic before for awarding badges
            user_methods.updateUpdatedProfilePic(the_user.uid)

        database.child("Users").child(u['localId']).update({"ProfilePic": newPic})  # set new profile pic in DB"""

    return returnUserProfileCarousels(request)


# method for updating only the background pic
def updateBackgroundPicRequest(request):
    if request.method == "POST":  # get data from UI
        newPic = request.POST.get("newPic")  # get data from UI using POST method

    global the_user  # edit the object value for profile pic
    the_user.backgroundPic = newPic

    database.child("Users").child(u['localId']).update({"BackgroundPic": newPic})  # set new profile pic in DB

    return returnUserProfileCarousels(request)


# checks the number of forums, courses and suggestions for the user profile and returns the appropriate data for the page to be loaded
def returnUserProfileCarousels(request):
    global the_user

    return render(request, "User_Profile_Page.html", {"e": email,
                                                      'n': the_user.username,
                                                      'bio': the_user.bio,
                                                      'email': the_user.email,
                                                      'country': the_user.country,
                                                      'ProfilePic': the_user.profilePic,
                                                      'backgroundPic': the_user.backgroundPic,
                                                      'course_list': course_methods.getCoursesInfoList(
                                                          the_user.uid, the_user.coursesInfoList[:3]),
                                                      'connections_suggestions_list': connection_methods.getConnectionsInfoList(
                                                          connection_methods.getConnectionsSuggestions(the_user.uid, 3, the_user)),
                                                      'forums_suggestions_list': forum_methods.getForumsInfoList(
                                                          forum_methods.getForumSuggestions(the_user.uid, 3, the_user)),
                                                      'this_uid': the_user.uid,
                                                      'enabled': user_methods.getUserEnabled(the_user.uid)
                                                      })


# Navigation Methods
def home(request):
    return returnUserProfileCarousels(request)


def forums(request):
    global the_user
    return render(request, 'ForumList.html', {'forums_list': forum_methods.getForumsInfoList(the_user.forumsInfoList),
                                              'email': the_user.email,
                                              'password': the_user.password,
                                              'my_country': the_user.country,
                                              'n': the_user.username,
                                              'ProfilePic': the_user.profilePic,
                                              'bio': the_user.bio,
                                              'my_forums_ids': convertArrayToString(the_user.forumsInfoList),
                                              'this_uid': the_user.uid,
                                              'username': the_user.username})


def courses(request):
    global the_user
    global short_course_suggestions
    all_courses = course_methods.getAllCoursesList(the_user.uid)

    return render(request, 'Courses.html', {'courses_list': course_methods.getCoursesInfoList(the_user.uid, the_user.coursesInfoList),
                                            'suggested_courses_list': course_methods.getCoursesInfoList(the_user.uid,
                                                short_course_suggestions),
                                            'this_uid': the_user.uid,
                                            'my_country': the_user.country,
                                            'n': the_user.username,
                                            'ProfilePic': the_user.profilePic,
                                            'bio': the_user.bio,
                                            'all_courses_list': course_methods.getCoursesInfoList(the_user.uid,
                                                all_courses),
                                            'email': the_user.email,
                                            'password': the_user.password,
                                            'my_course_ids': convertArrayToString(the_user.coursesInfoList),
                                            'all_courses_str': convertArrayToString(all_courses),
                                            'course_detail_list': course_methods.getCourseDetailsList(the_user.uid, all_courses)})


def goDirectMessaging(request):
    global the_user
    return render(request, 'DirectMessaging.html', {
                                            'this_uid': the_user.uid,
                                            'my_country': the_user.country,
                                            'n': the_user.username,
                                            'ProfilePic': the_user.profilePic,
                                            'bio': the_user.bio,
                                            'email': the_user.email,
                                            'password': the_user.password}
                  )


def connections(request):
    global the_user
    conn_suggestions = connection_methods.getConnectionsSuggestions(the_user.uid, 3, the_user)
    return render(request, 'Connections.html',
                  {#'connections_list': connection_methods.getConnectionsInfoList(the_user.connectionsInfoList),
                   #'suggested_connections_list': connection_methods.getConnectionsInfoList(
                    #   conn_suggestions)
                   'this_uid': the_user.uid,
                   'my_conn_ids': convertArrayToString(the_user.connectionsInfoList),
                   #'conn_suggestions_ids_str': convertArrayToString(conn_suggestions),
                   'my_country': the_user.country,
                   'n': the_user.username,
                   'ProfilePic': the_user.profilePic,
                   'bio': the_user.bio
                   })


def userprofile(request):
    return returnUserProfileCarousels(request)


def goSettings(request):
    global the_user
    global user_privacy
    global country_list
    return render(request, "Settings.html", {'profilePic': the_user.profilePic,
                                             'country': the_user.country,
                                             'username': the_user.username,
                                             'email': the_user.email,
                                             'bio': the_user.bio,
                                             'coursesPrivacy': user_privacy.courses,
                                             'bioPrivacy': user_privacy.bio,
                                             'forumsPrivacy': user_privacy.forums,
                                             'countryPrivacy': user_privacy.country,
                                             'connectionsPrivacy': user_privacy.connections,
                                             'total_country_list': country_list,
                                             'this_uid': the_user.uid,
                                             'enabled': user_methods.getUserEnabled(the_user.uid)

                                             })


def goBadges(request):
    # user authentication with Firebase
    name = user_methods.getUsername(u['localId'])
    conn = user_methods.getNumConnecions(u['localId'])
    privacyUpdate = user_methods.getPrivacyUpdated(u['localId'])

    global the_user

    return render(request, "Badges_Page.html", {
        'n': name,
        'country': the_user.country,
        'bio': the_user.bio,
        'profilePic': the_user.profilePic,
        'privacyUp': privacyUpdate,
        'numConnections': conn,
        'connections_suggestions_list': connection_methods.getConnectionsInfoList(
            connection_methods.getConnectionsSuggestions(the_user.uid, 3, the_user)),
        'forums_suggestions_list': forum_methods.getForumsInfoList(forum_methods.getForumSuggestions(the_user.uid, 3, the_user)),
        'enabled': user_methods.getUserEnabled(the_user.uid),
        'this_uid': the_user.uid
    })


def goHelpUserProfile(request):
    global the_user
    return render(request, "helpUserProfile.html", {'ProfilePic': the_user.profilePic,
                                               'n': the_user.username,
                                               'my_country': the_user.country,
                                                'bio': the_user.bio,})


def goHelpCourses(request):
    return render(request, "courseHelp.html", {'profilePic': the_user.profilePic,
                                               'country': the_user.country,
                                               'bio': the_user.bio,
                                               'n': the_user.username
                                               })


def goHelpConnections(request):
    return render(request, "connectionHelp.html", {'profilePic': the_user.profilePic})


def goIntroHelp(request):
    global the_user
    return render(request, 'introducingHelp.html',{'ProfilePic': the_user.profilePic,
                                               'n': the_user.username,
                                               'my_country': the_user.country,
                                               'bio': the_user.bio})


def goAccountHelp(request):
    global the_user
    return render(request, 'accountHelp.html', {'profilePic': the_user.profilePic,'n': the_user.username,
                                                'country': the_user.country,
                                                'bio': the_user.bio,
                                                'n': the_user.username
})


def goCreateForum(request):
    global the_user
    all_topics_list = ['Arts & Design', 'Business & Management', 'Education', 'Entrepreneurship', 'Executive Education', 'Finance', 'Health', 'Hospitality & Events', 'Law', 'Marketing', 'Project Management', 'Real Estate', 'Systems & Technology', 'Talent Management (HR)', 'Writing']

    return render(request, 'CreateForum.html', {'this_uid': the_user.uid,
                                                'profilePic': the_user.profilePic,
                                                'all_topics_list': all_topics_list,
                                                'n': the_user.username,
                                                'country': the_user.country,
                                                'bio': the_user.bio,


                                                })

def goForumsHelp(request):
    return render(request, 'ForumsHelp.html', {'ProfilePic': the_user.profilePic,
                                               'n': the_user.username,
                                               'my_country': the_user.country,
                                                'bio': the_user.bio,

    })


def goForumsOpen(request):
    global the_user
    global short_forum_suggestions

    forum_id = ""
    if request.method == "POST":  # get data from UI
        forum_id = request.POST.get("forum_id")  # get data from UI using POST method

    return render(request, "ForumsMessaging.html", {'profilePic': the_user.profilePic,
                                                    'forum_id': forum_id,
                                             'country': the_user.country,
                                             'username': the_user.username,
                                             'email': the_user.email,
                                             'bio': the_user.bio,
                                             'this_uid': the_user.uid,
                                             'my_forums_list': forum_methods.getForumsInfoList(user_methods.getForumssList(the_user.uid)),
                                                    'forum_name': forum_methods.getForumName(forum_id),
                                                    'forum_description': forum_methods.getForumDescription(forum_id),
                                                    'num_participants': forum_methods.getForumNumParticipants(forum_id),
                                                    'forum_topics': forum_methods.getForumTopicsString(forum_id),
                                                    'forum_creator': forum_methods.getForumCreator(forum_id),
                                                    'forum_pic': forum_methods.getForumPic(forum_id),
                                                    'forum_enabled': forum_methods.getForumEnabled(forum_id)
                                             })
def goForumSettings(request):
    global the_user

    forum_id = ""
    if request.method == "POST":  # get data from UI
        forum_id = request.POST.get("forum_id")  # get data from UI using POST method

    all_topics_list = ['Arts & Design', 'Business & Management', 'Education', 'Entrepreneurship', 'Executive Education', 'Finance', 'Health', 'Hospitality & Events', 'Law', 'Marketing', 'Project Management', 'Real Estate', 'Systems & Technology', 'Talent Management (HR)', 'Writing']

    return render(request, "ForumSettings.html", {'profilePic': the_user.profilePic,
                                                    'forum_id': forum_id,
                                                    'country': the_user.country,
                                                    'username': the_user.username,
                                                    'email': the_user.email,
                                                    'bio': the_user.bio,
                                                    'this_uid': the_user.uid,
                                                    'my_forums_list': forum_methods.getForumsInfoList(
                                                        the_user.forumsInfoList),
                                                    'suggested_forums_list': forum_methods.getForumsInfoList(
                                                        short_forum_suggestions),
                                                    'forum_name': forum_methods.getForumName(forum_id),
                                                    'forum_description': forum_methods.getForumDescription(forum_id),
                                                    'num_participants': forum_methods.getForumNumParticipants(forum_id),
                                                    #'forum_topics_str': forum_methods.getForumTopicsString(forum_id),
                                                    'forum_topics_list': forum_methods.getForumTopicsList(forum_id),
                                                    'forum_creator': forum_methods.getForumCreator(forum_id),
                                                    'forum_pic': forum_methods.getForumPic(forum_id),
                                                    'forum_enabled': forum_methods.getForumEnabled(forum_id),
                                                    'forum_private': forum_methods.getForumPrivate(forum_id),
                                                    'all_topics_list': all_topics_list
                                                    })

def goConnectionsOpen(request):
    global the_user

    # dummy forums and courses for when forums and courses are private - do NOT add these to the database
    dummy_image_url = "https://i1.wp.com/wrbbradio.org/wp-content/uploads/2016/10/grey-background-06.jpg?fit=2560%2C1600"
    dummy_forum_list = ["Forum Private", dummy_image_url, "-", "", "", "", ""]
    dummy_course_list = ["Course is Private", dummy_image_url, "", "", "", "", "", "", ""]

    connection_id = ""
    if request.method == "POST":  # get data from UI
        connection_id = request.POST.get("connection_id")  # get data from UI using POST method

    privacyUpdate = user_methods.getPrivacyUpdated(connection_id)

    # get mutual connections and check if this user is a connection
    selected_user_connections = user_methods.getUserConnectionsList(connection_id)       # get a list of the selected user's connections
    logged_in_user_connections = user_methods.getUserConnectionsList(the_user.uid)       # get the connections of the user who is logged in
    the_user_is_connection = False
    mutual_connections = []

    if selected_user_connections is not None:
        for connection in selected_user_connections:
            if forum_methods.arrayContainsValue(logged_in_user_connections, connection):                                     # if this connection is in the logged iin user's connections list
                mutual_connections.append(connection)
            elif connection == the_user.uid:                                                   # check if the user logged in is a connect
                the_user_is_connection = True

    # check privacy settings of connection before displaying their information
    if user_methods.getBioPrivacy(connection_id) == "True":
        bio = "Bio is Private"
    else:
        bio = user_methods.getBio(connection_id)

    if user_methods.getForumsPrivacy(connection_id) == "True":
        # places dummy values in the list to indicate that the user's forums are private
        forums_list_transfer = [dummy_forum_list, dummy_forum_list, dummy_forum_list]
    else:
        forums_list_transfer = forum_methods.getForumsInfoList(user_methods.getForumssList(connection_id)[:3])

    if user_methods.getCoursesPrivacy(connection_id) == "True":
        courses_list_transfer = [dummy_course_list, dummy_course_list, dummy_course_list]
    else:
        courses_list_transfer = course_methods.getCoursesInfoList(
                                                          the_user.uid, user_methods.getCoursesList(connection_id)[:3])

    if user_methods.getCountryPrivacy(connection_id) == "True":
        country_transfer = "Country is Private"
    else:
        country_transfer = user_methods.getCountry(connection_id)

    if user_methods.getPicPrivacy(connection_id) == "True":
        pic_transfer = "https://firebasestorage.googleapis.com/v0/b/getconnected-9dac0.appspot.com/o/images%2FprofilePics%2FdefaultProfilePic.png?alt=media&token=ef77ab0a-8776-47fa-8894-ff79c659bcb3"
    else:
        pic_transfer = user_methods.getProfilePic(connection_id)

    return render(request, "User_Profile_Page_Visiting.html", {"e": "MZVWIN001@myuct.ac.za",
                                                      'n': user_methods.getUsername(connection_id),
                                                      'bio': bio,
                                                      'email': "MZVWIN001@myuct.ac.za",
                                                      'country': country_transfer,
                                                      'numConnections': user_methods.getNumConnecions(
                                                                   connection_id),
                                                      'ProfilePic': pic_transfer,
                                                      'my_profile_pic': the_user.profilePic,
                                                      'backgroundPic': user_methods.getBackgroundPic(connection_id),
                                                      'course_list': courses_list_transfer,
                                                      'forums_list': forums_list_transfer,
                                                      'connections_suggestions_list': connection_methods.getConnectionsInfoList(
                                                        connection_methods.getConnectionsSuggestions(the_user.uid, 3, the_user)),
                                                      'forums_suggestions_list': forum_methods.getForumsInfoList(forum_methods.getForumSuggestions(the_user.uid, 3, the_user)),
                                                      'this_uid': connection_id,
                                                      'my_uid': the_user.uid,
                                                      'the_user_is_connection': the_user_is_connection,
                                                      'privacyUp': privacyUpdate,
                                                      'mutual_connections': connection_methods.getConnectionsInfoList(connection_methods.getMutualConnections(connection_id, the_user.uid))
                                                      })



def goContact(request):
    return render(request, 'contactus.html')


def goTemp(request):
    return render(request, 'Temporary.html')


# search and filter functions

def getSearchByTopic(request):
    # search list received by the post method
    if request.method == "POST":
        topic = request.POST.get("topic")
        courses_list = request.POST.getlist("course_list")
        suggested_courses = request.POST.getlist("suggested_courses_list")

    global the_user
    the_user.coursesInfoList = courses_list

    # unzip all lists
    course_names, course_pictures, course_recommendations, course_urls, course_uni_pics, courses_ids, course_topics, course_uni = zip(
        *courses_list)

    # code to search by topic
    # remove item from all lists if they don't contain the topic

    # zip all lists back
    filtered_courses_list = zip(course_names, course_pictures, course_recommendations, course_urls, course_uni_pics,
                                courses_ids, course_topics, course_uni)

    return render(request, 'Courses.html', {'courses_list': filtered_courses_list,
                                            'suggested_courses_list': suggested_courses})  # return and render courses page with filtered list


def heartCourse(request):
    if request.method == "POST":
            course_id = request.POST.get("course_id")                   # get the id of the course that is being hearted
            num_rec = int(course_methods.getCourseNumRecommendations(
                course_id)) + 1                                         # add 1 to the number of course recommendations for the selected course
            course_methods.updateCourseNumRecommendations(course_id, num_rec)


def unheartCourse(request):
    if request.method == "POST":
            course_id = request.POST.get("course_id")                   # get the id of the course that is being hearted
            num_rec = int(course_methods.getCourseNumRecommendations(
                course_id)) - 1                                         # subtract 1 to the number of course recommendations for the selected course
            course_methods.updateCourseNumRecommendations(course_id, num_rec)


country_list = ['None', "Afghanistan", "ÅlandIslands", "Albania", "Algeria", "AmericanSamoa", "Andorra", "Angola",
                "Anguilla",
                "Antarctica", "AntiguaandBarbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria",
                "Azerbaijan",
                "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda",
                "Bhutan",
                "Bolivia", "BosniaandHerzegovina", "Botswana", "BouvetIsland", "Brazil", "BritishIndianOceanTerritory",
                "BruneiDarussalam", "Bulgaria", "BurkinaFaso", "Burundi", "Cambodia", "Cameroon", "Canada", "CapeVerde",
                "CaymanIslands", "CentralAfricanRepublic", "Chad", "Chile", "China", "ChristmasIsland",
                "Cocos(Keeling)Islands", "Colombia", "Comoros", "Congo", "Congo,TheDemocraticRepublicofThe",
                "CookIslands", "CostaRica", "CoteD'ivoire", "Croatia", "Cuba", "Cyprus", "CzechRepublic", "Denmark",
                "Djibouti", "Dominica", "DominicanRepublic", "Ecuador", "Egypt", "ElSalvador", "EquatorialGuinea",
                "Eritrea", "Estonia", "Ethiopia", "FalklandIslands(Malvinas)""FaroeIslands", "Fiji", "Finland",
                "France", "FrenchGuiana", "FrenchPolynesia", "FrenchSouthernTerritories", "Gabon", "Gambia", "Georgia",
                "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala",
                "Guernsey", "Guinea", "Guinea-bissau", "Guyana", "Haiti", "HeardIslandandMcdonaldIslands",
                "HolySee(VaticanCityState)", "Honduras", "HongKong", "Hungary", "Iceland", "India", "Indonesia",
                "IslamicRepublicofIran", "Iraq", "Ireland", "IsleofMan", "Israel", "Italy", "Jamaica", "Japan",
                "Jersey", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "DemocraticPeople'sRepublicofKorea",
                "RepublicofKorea", "Kuwait", "Kyrgyzstan", "LaoPeople'sDemocraticRepublic", "Latvia", "Lebanon",
                "Lesotho", "Liberia", "LibyanArabJamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macao",
                "TheFormerYugoslavRepublicofMacedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
                "MarshallIslands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico",
                "FederatedStatesofMicronesia", "RepublicofMoldova", "Monaco", "Mongolia", "Montenegro", "Montserrat",
                "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "NetherlandsAntilles",
                "NewCaledonia", "NewZealand", "Nicaragua", "Niger", "Nigeria", "Niue", "NorfolkIsland",
                "NorthernMarianaIslands", "Norway", "Oman", "Pakistan", "Palau", "PalestinianTerritory""Panama",
                "PapuaNewGuinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "PuertoRico",
                "Qatar", "Reunion", "Romania", "RussianFederation", "Rwanda", "SaintHelena", "SaintKittsandNevis",
                "SaintLucia", "SaintPierreandMiquelon", "SaintVincentandTheGrenadines", "Samoa", "SanMarino",
                "SaoTomeandPrincipe", "SaudiArabia", "Senegal", "Serbia", "Seychelles", "SierraLeone", "Singapore",
                "Slovakia", "Slovenia", "SolomonIslands", "Somalia", "SouthAfrica",
                "SouthGeorgiaandTheSouthSandwichIslands", "Spain", "SriLanka", "Sudan", "Suriname",
                "SvalbardandJanMayen", "Swaziland", "Sweden", "Switzerland", "SyrianArabRepublic",
                "Taiwan,ProvinceofChina", "Tajikistan", "Tanzania,UnitedRepublicofCongo", "Thailand", "Timor-leste",
                "Togo", "Tokelau", "Tonga", "TrinidadandTobago", "Tunisia", "Turkey", "Turkmenistan",
                "TurksandCaicosIslands", "Tuvalu", "Uganda", "Ukraine", "UnitedArabEmirates", "UnitedKingdom",
                "UnitedStates", "UnitedStatesMinorOutlyingIslands", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela",
                "VietNam", "VirginIslands,British", "VirginIslands,U.S.", "WallisandFutuna", "WesternSahara", "Yemen",
                "Zambia", "Zimbabwe"]


# method that converts and array to a string with a , as a delimiter between each item
def convertArrayToString(arr):
    arrString = ""
    if arr is not None:
        for item in arr:
            arrString = arrString + "," + item
    else:
        arrString = ""
    return arrString
