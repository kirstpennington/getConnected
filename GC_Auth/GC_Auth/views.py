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

the_user = ""       # object to store user information
user_privacy = ""   # object to store user privacy information

email = ""

short_connections_suggestions = ""
short_forum_suggestions = ""



# LOGIN methods

def LogIn(request):
    forum_names, forum_pics, forum_num_participants, forum_creators, forum_topics, forum_descriptions, forum_ids = zip(*forum_methods.getTrendingForums(""))        # unzip all elements of each trending forum

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
    return render(request,"passwordReset.html")


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

    global the_user     # create the_user object to store user profile data

    # if the user image or background is blank, set it to a default value
    if user_methods.getBackgroundPic(user['localId']) == "":
        user_methods.updateBackgroundPic(user['localId'],"https://cdn.shopify.com/s/files/1/2656/8500/products/galerie-wallpapers-unplugged-textured-plain-grey-wallpaper-2035691716651_1024x.jpg?v=1522251583")
        the_user.backgroundPic = "https://cdn.shopify.com/s/files/1/2656/8500/products/galerie-wallpapers-unplugged-textured-plain-grey-wallpaper-2035691716651_1024x.jpg?v=1522251583"

    if user_methods.getProfilePic(user['localId']) == "":
        user_methods.updateProfilePic(user['localId'],  "https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg" )
        the_user.profilePic = "https://eduexcellencestaff.co.za/wp-content/uploads/2018/09/default-profile.jpg"

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
                    course_methods.getCoursesInfoList(user_methods.getCoursesList(user['localId'])),
                    forum_methods.getForumsInfoList(user_methods.getForumssList(user['localId'])),
                    user_methods.getUserTopicsList(user['localId'])
                    )


    global user_privacy # create user_privacy object to store user privacy data
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
    return render(request, 'LogIn.html')


def getPrivacySettings(request):
    # Name of html file to be changed
        return render(request, "PrivacySettings.html", {'bioPrivacy': user_privacy.bio,
                                                        'connectionPrivacy': user_privacy.connections,
                                                        'countryPrivacy': user_privacy.country,
                                                        'namePrivacy': user_privacy.name,
                                                        'pPicPrivacy': user_privacy.pic,
                                                        })


# Called to update Profile Page from Settings.html page - leads to User Profile page
def updateProfile(request):
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

        print("Country", country)  # Country South - space issue
        print("bio", bio)  # Country South - space issue
        print("course privacy", coursesPrivacy)  # Country South - space issue
        print("forums privacy", forumsPrivacy)  # Country South - space issue

        global the_user
        global user_privacy

        if the_user.username != name:                         # check is there was a change made first
            user_methods.updateUsername(the_user.uid, name)   # call each method to update elements of the profile in the db
            the_user.username = name                          # edit the contents of the the_user variable

        if the_user.bio != bio:
            user_methods.updateBio(the_user.uid, bio)
            the_user.bio = bio

        if the_user.country != country:
            user_methods.updateCountry(the_user.uid, country)
            the_user.country = country

        if the_user.email != email:
            user_methods.updateEmail(the_user.uid, email)
            the_user.email = email

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
    return returnUserProfileCarousels(request)                  # render user profile with updated data


"""def updatePrivacySettings(request):
    if request.method == "POST":
        # get data from UI using POST method
        bioPrivacy = request.POST.get("bioPrivacy")
        connectionPrivacy = request.POST.get("connectionPrivacy")
        countryPrivacy = request.POST.get("countryPrivacy")
        namePrivacy = request.POST.get("namePrivacy")
        pPicPrivacy = request.POST.get("pPicPrivacy")
        coursesPrivacy = request.POST.get("coursesPrivacy")
        forumsPrivacy = request.POST.get("forumsPrivacy")

    global the_user
    # call each method to update elements of the profile in the db
    user_methods.updateBioPrivacy(the_user.uid, bioPrivacy)
    user_methods.updateConnectionPrivacy(the_user.uid, connectionPrivacy)
    user_methods.updateCountryPrivacy(the_user.uid, countryPrivacy)
    user_methods.updateNamePrivacy(the_user.uid, namePrivacy)
    user_methods.updatePicPrivacy(the_user.uid, pPicPrivacy)
    user_methods.updateCoursesPrivacy(the_user.uid, coursesPrivacy)
    user_methods.updateForumsPrivacy(the_user.uid, forumsPrivacy)

    global user_privacy
    user_privacy.bio = bioPrivacy
    user_privacy.connections = connectionPrivacy
    user_privacy.country = countryPrivacy
    user_privacy.name = namePrivacy
    user_privacy.pic = pPicPrivacy
    user_privacy.courses = coursesPrivacy
    user_privacy.forums = forumsPrivacy

    # edit return render to show the new data
    return render(request, "User_Profile_Page.html", {'bioPrivacy': bioPrivacy,
                                                'connectionPrivacy': connectionPrivacy,
                                                'countryPrivacy': countryPrivacy,
                                                'namePrivacy': namePrivacy,
                                                'pPicPrivacy': pPicPrivacy,
                                                'coursesPrivacy': coursesPrivacy,
                                                'forumsPrivacy': forumsPrivacy
                                                })"""


# method for updating only the profile pic
def updateProfilePicRequest(request):
    if request.method == "POST":                                # get data from UI
        newPic = request.POST.get("newPic")                     # get data from UI using POST method

    global the_user                                             # edit the object value for profile pic
    the_user.profilePic = newPic

    if user_methods.getUpdatedProfilePic(
            the_user.uid) != "yes":                             # tracks whether the user has updated their profile pic before for awarding badges
        user_methods.updateUpdatedProfilePic(the_user.uid)

    database.child("Users").child(u['localId']).update({"ProfilePic": newPic})  # set new profile pic in DB

    return returnUserProfileCarousels(request)


# method for updating only the background pic
def updateBackgroundPicRequest(request):
    if request.method == "POST":                                # get data from UI
        newPic = request.POST.get("newPic")                     # get data from UI using POST method

    global the_user                                             # edit the object value for profile pic
    the_user.backgroundPic = newPic

    database.child("Users").child(u['localId']).update({"BackgroundPic": newPic})       # set new profile pic in DB

    return returnUserProfileCarousels(request)


# checks the number of forums, courses and suggestions for the user profile and returns the appropriate data for the page to be loaded
def returnUserProfileCarousels(request):
    global the_user

    """global short_forum_suggestions      # if the suggested forums has not been determined yet
    if short_forum_suggestions == "":
        short_forum_suggestions = forum_methods.getForumSuggestions(the_user.uid, 5, the_user)

    global short_connections_suggestions  # if the suggested forums has not been determined yet
    if short_connections_suggestions == "":
        short_connections_suggestions = connection_methods.getConnectionsSuggestions(the_user.uid, 5, the_user)"""

    return render(request, "User_Profile_Page.html", {"e": email,
                                                      'n': the_user.username,
                                                      'bio': the_user.bio,
                                                      'email': the_user.email,
                                                      'country': the_user.country,
                                                      'numConnections': the_user.numConnections,
                                                      'numForums': the_user.numForums,
                                                      'ProfilePic': the_user.profilePic,
                                                      'backgroundPic': the_user.backgroundPic,
                                                      'course_list': course_methods.getCoursesInfoList(
                                                            user_methods.getCoursesList(the_user.uid)),
                                                      'forums_list': forum_methods.getForumsInfoList(user_methods.getForumssList(the_user.uid)),
                                                      'connections_suggestions_list': connection_methods.getConnectionsSuggestions(the_user.uid, 5, the_user),
                                                      'forums_suggestions_list': forum_methods.getForumSuggestions(the_user.uid, 5, the_user)
                                                      })


# Navigation Methods
def home(request):
    return returnUserProfileCarousels(request)


def networks(request):
    return render(request, 'MyNetwork.html')


def forums(request):
    global the_user
    global short_forum_suggestions
    return render(request, 'Forums.html', {'forums_list': the_user.forumsInfoList,
                                           'suggested_forums_list': short_forum_suggestions})


def courses(request):
    global the_user
    courses_list = course_methods.getCoursesInfoList(user_methods.getCoursesList(the_user.uid))
    suggested_courses = course_methods.getCourseSuggestions(the_user.uid, 3, the_user)
    # course_names, course_pictures, course_recommendations, course_urls, course_uni_pics = zip(*suggested_courses)
    # print(course_names)
    return render(request, 'Courses.html', {'courses_list': courses_list,
                                            'suggested_courses_list': suggested_courses})


def connections(request):
    global the_user
    return render(request, 'Connections.html', {'connections_list': connection_methods.getConnectionsInfoList(user_methods.getUserConnectionsList(the_user.uid)),
                                                'suggested_connections_list': connection_methods.getConnectionsSuggestions(the_user, 3)})


def userprofile(request):
    return returnUserProfileCarousels(request)


def goSettings(request):
    global the_user
    global user_privacy
    global country_list
    print(user_privacy.courses, user_privacy.forums)
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
                                             'total_country_list': country_list
                                            })


def goBadges(request):
    # user authentication with Firebase
    name = user_methods.getUsername(u['localId'])
    conn = user_methods.getNumConnecions(u['localId'])
    course = user_methods.getNumCourses(u['localId'])
    forum = user_methods.getNumForums(u['localId'])
    privacyUpdate = user_methods.getPrivacyUpdated(u['localId'])

    global short_connections_suggestions
    global short_connections_suggestions
    global the_user

    return render(request, "badgesStart.html", {
            'n': name,
            'numConnections': conn,
            'numCourses': course,
            'numForums': forum,
            'privacyUp': privacyUpdate,
            'connections_suggestions_list': connection_methods.getConnectionsSuggestions(the_user.uid, 5, the_user),
            'forums_suggestions_list': forum_methods.getForumSuggestions(the_user.uid, 5, the_user)
    })


def goHelpUserProfile(request):
    return render(request, "helpUserProfile.html")


def goIntroHelp(request):
    return render(request, 'introducingHelp.html')


def goAccountHelp(request):
    return render(request, 'accountHelp.html')


def goForumsOpen(request):
    return render(request, 'ForumsOpen.html')


def goContact(request):
    return render(request, 'contactus.html')



# search and filter functions

def getSearchByTopic(request):
    # search list received by the post method
    print("I'm here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if request.method == "POST":
        topic = request.POST.get("topic")
        courses_list = request.POST.getlist("course_list")
        suggested_courses = request.POST.getlist("suggested_courses_list")

    global the_user
    the_user.coursesInfoList = courses_list

    # unzip all lists
    course_names, course_pictures, course_recommendations, course_urls, course_uni_pics, courses_ids, course_topics, course_uni = zip(*courses_list)

    # code to search by topic
    # remove item from all lists if they don't contain the topic

    # zip all lists back
    filtered_courses_list = zip(course_names, course_pictures, course_recommendations, course_urls, course_uni_pics, courses_ids, course_topics, course_uni)

    return render(request, 'Courses.html', {'courses_list': filtered_courses_list,
                                            'suggested_courses_list': suggested_courses})       # return and render courses page with filtered list


country_list = ['None',
                "Afghanistan",
                "Åland Islands",
                "Albania",
                "Algeria",
                "AmericanSamoa",
                "Andorra",
                "Angola",
                "Anguilla",
                "Antarctica",
                "AntiguaandBarbuda",
                "Argentina",
                "Armenia",
                "Aruba",
                "Australia",
                "Austria",
                "Azerbaijan",
                "Bahamas",
                "Bahrain",
                "Bangladesh",
                "Barbados",
                "Belarus",
                "Belgium",
                "Belize",
                "Benin",
                "Bermuda",
                "Bhutan",
                "Bolivia",
                "BosniaandHerzegovina",
                "Botswana",
                "BouvetIsland",
                "Brazil",
                "BritishIndianOceanTerritory",
                "BruneiDarussalam",
                "Bulgaria",
                "BurkinaFaso",
                "Burundi",
                "Cambodia",
                "Cameroon",
                "Canada",
                "CapeVerde",
                "CaymanIslands",
                "CentralAfricanRepublic",
                "Chad",
                "Chile",
                "China",
                "Christmas Island",
                "Cocos(Keeling)Islands",
                "Colombia",
                "Comoros",
                "Congo",
                "Congo, The Democratic Republic of The ",
                "Cook Islands",
                "Costa Rica",
                "CoteD'ivoire",
                "Croatia",
                "Cuba",
                "Cyprus",
                "Czech Republic",
                "Denmark",
                "Djibouti",
                "Dominica",
                "Dominican Republic",
                "Ecuador",
                "Egypt",
                "El Salvador",
                "Equatorial Guinea",
                "Eritrea",
                "Estonia",
                "Ethiopia",
                "Falkland Islands(Malvinas)"
                "Faroe Islands",
                "Fiji",
                "Finland",
                "France",
                "French Guiana",
                "French Polynesia",
                "French Southern Territories",
                "Gabon",
                "Gambia",
                "Georgia",
                "Germany",
                "Ghana",
                "Gibraltar",
                "Greece",
                "Greenland",
                "Grenada",
                "Guadeloupe",
                "Guam",
                "Guatemala",
                "Guernsey",
                "Guinea",
                "Guinea-bissau",
                "Guyana",
                "Haiti",
                "Heard Island and Mcdonald Islands",
                "HolySee(Vatican City State)",
                "Honduras",
                "Hong Kong",
                "Hungary",
                "Iceland",
                "India",
                "Indonesia",
                "Islamic Republic of Iran",
                "Iraq",
                "Ireland",
                "Isle of Man",
                "Israel",
                "Italy",
                "Jamaica",
                "Japan",
                "Jersey",
                "Jordan",
                "Kazakhstan",
                "Kenya",
                "Kiribati",
                "Democratic People's Republic of Korea",
                "Republic of Korea",
                "Kuwait",
                "Kyrgyzstan",
                "Lao People's Democratic Republic",
                "Latvia",
                "Lebanon",
                "Lesotho",
                "Liberia",
                "Libyan Arab Jamahiriya",
                "Liechtenstein",
                "Lithuania",
                "Luxembourg",
                "Macao",
                "The Former Yugoslav Republic of Macedonia",
                "Madagascar",
                "Malawi",
                "Malaysia",
                "Maldives",
                "Mali",
                "Malta",
                "Marshall Islands",
                "Martinique",
                "Mauritania",
                "Mauritius",
                "Mayotte",
                "Mexico",
                "Federated States of Micronesia",
                "Republic of Moldova",
                "Monaco",
                "Mongolia",
                "Montenegro",
                "Montserrat",
                "Morocco",
                "Mozambique",
                "Myanmar",
                "Namibia",
                "Nauru",
                "Nepal",
                "Netherlands",
                "Netherlands Antilles",
                "New Caledonia",
                "New Zealand",
                "Nicaragua",
                "Niger",
                "Nigeria",
                "Niue",
                "Norfolk Island",
                "Northern Mariana Islands",
                "Norway",
                "Oman",
                "Pakistan",
                "Palau",
                "Palestinian Territory"
                "Panama",
                "Papua New Guinea",
                "Paraguay",
                "Peru",
                "Philippines",
                "Pitcairn",
                "Poland",
                "Portugal",
                "Puerto Rico",
                "Qatar",
                "Reunion",
                "Romania",
                "Russian Federation",
                "Rwanda",
                "Saint Helena",
                "Saint Kitts and Nevis",
                "Saint Lucia",
                "Saint Pierre and Miquelon",
                "Saint Vincent and The Grenadines",
                "Samoa",
                "San Marino",
                "Sao Tomeand Principe",
                "Saudi Arabia",
                "Senegal",
                "Serbia",
                "Seychelles",
                "Sierra Leone",
                "Singapore",
                "Slovakia",
                "Slovenia",
                "Solomon Islands",
                "Somalia",
                "South Africa",
                "South Georgia and TheSouth Sandwich Islands",
                "Spain",
                "SriLanka",
                "Sudan",
                "Suriname",
                "Svalbard and Jan Mayen",
                "Swaziland",
                "Sweden",
                "Switzerland",
                "SyrianArabRepublic",
                "Taiwan,Province of China",
                "Tajikistan",
                "Tanzania,United Republic of Congo",
                "Thailand",
                "Timor-leste",
                "Togo",
                "Tokelau",
                "Tonga",
                "TrinidadandTobago",
                "Tunisia",
                "Turkey",
                "Turkmenistan",
                "TurksandCaicosIslands",
                "Tuvalu",
                "Uganda",
                "Ukraine",
                "UnitedArabEmirates",
                "UnitedKingdom",
                "UnitedStates",
                "UnitedStatesMinorOutlyingIslands",
                "Uruguay",
                "Uzbekistan",
                "Vanuatu",
                "Venezuela",
                "VietNam",
                "VirginIslands,British",
                "VirginIslands,U.S.",
                "WallisandFutuna",
                "WesternSahara",
                "Yemen",
                "Zambia",
                "Zimbabwe"]

""" <option value="Åland Islands">Åland Islands</option>
                <option value="Albania">Albania</option>
                <option value="Algeria">Algeria</option>
                <option value="American Samoa">American Samoa</option>
                <option value="Andorra">Andorra</option>
                <option value="Angola">Angola</option>
                <option value="Anguilla">Anguilla</option>
                <option value="Antarctica">Antarctica</option>
                <option value="Antigua and Barbuda">Antigua and Barbuda</option>
                <option value="Argentina">Argentina</option>
                <option value="Armenia">Armenia</option>
                <option value="Aruba">Aruba</option>
                <option value="Australia">Australia</option>
                <option value="Austria">Austria</option>
                <option value="Azerbaijan">Azerbaijan</option>
                <option value="Bahamas">Bahamas</option>
                <option value="Bahrain">Bahrain</option>
                <option value="Bangladesh">Bangladesh</option>
                <option value="Barbados">Barbados</option>
                <option value="Belarus">Belarus</option>
                <option value="Belgium">Belgium</option>
                <option value="Belize">Belize</option>
                <option value="Benin">Benin</option>
                <option value="Bermuda">Bermuda</option>
                <option value="Bhutan">Bhutan</option>
                <option value="Bolivia">Bolivia</option>
                <option value="Bosnia and Herzegovina">Bosnia and Herzegovina</option>
                <option value="Botswana">Botswana</option>
                <option value="Bouvet Island">Bouvet Island</option>
                <option value="Brazil">Brazil</option>
                <option value="British Indian Ocean Territory">British Indian Ocean Territory</option>
                <option value="Brunei Darussalam">Brunei Darussalam</option>
                <option value="Bulgaria">Bulgaria</option>
                <option value="Burkina Faso">Burkina Faso</option>
                <option value="Burundi">Burundi</option>
                <option value="Cambodia">Cambodia</option>
                <option value="Cameroon">Cameroon</option>
                <option value="Canada">Canada</option>
                <option value="Cape Verde">Cape Verde</option>
                <option value="Cayman Islands">Cayman Islands</option>
                <option value="Central African Republic">Central African Republic</option>
                <option value="Chad">Chad</option>
                <option value="Chile">Chile</option>
                <option value="China">China</option>
                <option value="Christmas Island">Christmas Island</option>
                <option value="Cocos (Keeling) Islands">Cocos (Keeling) Islands</option>
                <option value="Colombia">Colombia</option>
                <option value="Comoros">Comoros</option>
                <option value="Congo">Congo</option>
                <option value="Congo, The Democratic Republic of The">Congo, The Democratic Republic of The</option>
                <option value="Cook Islands">Cook Islands</option>
                <option value="Costa Rica">Costa Rica</option>
                <option value="Cote D'ivoire">Cote D'ivoire</option>
                <option value="Croatia">Croatia</option>
                <option value="Cuba">Cuba</option>
                <option value="Cyprus">Cyprus</option>
                <option value="Czech Republic">Czech Republic</option>
                <option value="Denmark">Denmark</option>
                <option value="Djibouti">Djibouti</option>
                <option value="Dominica">Dominica</option>
                <option value="Dominican Republic">Dominican Republic</option>
                <option value="Ecuador">Ecuador</option>
                <option value="Egypt">Egypt</option>
                <option value="El Salvador">El Salvador</option>
                <option value="Equatorial Guinea">Equatorial Guinea</option>
                <option value="Eritrea">Eritrea</option>
                <option value="Estonia">Estonia</option>
                <option value="Ethiopia">Ethiopia</option>
                <option value="Falkland Islands (Malvinas)">Falkland Islands (Malvinas)</option>
                <option value="Faroe Islands">Faroe Islands</option>
                <option value="Fiji">Fiji</option>
                <option value="Finland">Finland</option>
                <option value="France">France</option>
                <option value="French Guiana">French Guiana</option>
                <option value="French Polynesia">French Polynesia</option>
                <option value="French Southern Territories">French Southern Territories</option>
                <option value="Gabon">Gabon</option>
                <option value="Gambia">Gambia</option>
                <option value="Georgia">Georgia</option>
                <option value="Germany">Germany</option>
                <option value="Ghana">Ghana</option>
                <option value="Gibraltar">Gibraltar</option>
                <option value="Greece">Greece</option>
                <option value="Greenland">Greenland</option>
                <option value="Grenada">Grenada</option>
                <option value="Guadeloupe">Guadeloupe</option>
                <option value="Guam">Guam</option>
                <option value="Guatemala">Guatemala</option>
                <option value="Guernsey">Guernsey</option>
                <option value="Guinea">Guinea</option>
                <option value="Guinea-bissau">Guinea-bissau</option>
                <option value="Guyana">Guyana</option>
                <option value="Haiti">Haiti</option>
                <option value="Heard Island and Mcdonald Islands">Heard Island and Mcdonald Islands</option>
                <option value="Holy See (Vatican City State)">Holy See (Vatican City State)</option>
                <option value="Honduras">Honduras</option>
                <option value="Hong Kong">Hong Kong</option>
                <option value="Hungary">Hungary</option>
                <option value="Iceland">Iceland</option>
                <option value="India">India</option>
                <option value="Indonesia">Indonesia</option>
                <option value="Iran, Islamic Republic of">Iran, Islamic Republic of</option>
                <option value="Iraq">Iraq</option>
                <option value="Ireland">Ireland</option>
                <option value="Isle of Man">Isle of Man</option>
                <option value="Israel">Israel</option>
                <option value="Italy">Italy</option>
                <option value="Jamaica">Jamaica</option>
                <option value="Japan">Japan</option>
                <option value="Jersey">Jersey</option>
                <option value="Jordan">Jordan</option>
                <option value="Kazakhstan">Kazakhstan</option>
                <option value="Kenya">Kenya</option>
                <option value="Kiribati">Kiribati</option>
                <option value="Korea, Democratic People's Republic of">Korea, Democratic People's Republic of</option>
                <option value="Korea, Republic of">Korea, Republic of</option>
                <option value="Kuwait">Kuwait</option>
                <option value="Kyrgyzstan">Kyrgyzstan</option>
                <option value="Lao People's Democratic Republic">Lao People's Democratic Republic</option>
                <option value="Latvia">Latvia</option>
                <option value="Lebanon">Lebanon</option>
                <option value="Lesotho">Lesotho</option>
                <option value="Liberia">Liberia</option>
                <option value="Libyan Arab Jamahiriya">Libyan Arab Jamahiriya</option>
                <option value="Liechtenstein">Liechtenstein</option>
                <option value="Lithuania">Lithuania</option>
                <option value="Luxembourg">Luxembourg</option>
                <option value="Macao">Macao</option>
                <option value="Macedonia, The Former Yugoslav Republic of">Macedonia, The Former Yugoslav Republic of
                </option>
                <option value="Madagascar">Madagascar</option>
                <option value="Malawi">Malawi</option>
                <option value="Malaysia">Malaysia</option>
                <option value="Maldives">Maldives</option>
                <option value="Mali">Mali</option>
                <option value="Malta">Malta</option>
                <option value="Marshall Islands">Marshall Islands</option>
                <option value="Martinique">Martinique</option>
                <option value="Mauritania">Mauritania</option>
                <option value="Mauritius">Mauritius</option>
                <option value="Mayotte">Mayotte</option>
                <option value="Mexico">Mexico</option>
                <option value="Micronesia, Federated States of">Micronesia, Federated States of</option>
                <option value="Moldova, Republic of">Moldova, Republic of</option>
                <option value="Monaco">Monaco</option>
                <option value="Mongolia">Mongolia</option>
                <option value="Montenegro">Montenegro</option>
                <option value="Montserrat">Montserrat</option>
                <option value="Morocco">Morocco</option>
                <option value="Mozambique">Mozambique</option>
                <option value="Myanmar">Myanmar</option>
                <option value="Namibia">Namibia</option>
                <option value="Nauru">Nauru</option>
                <option value="Nepal">Nepal</option>
                <option value="Netherlands">Netherlands</option>
                <option value="Netherlands Antilles">Netherlands Antilles</option>
                <option value="New Caledonia">New Caledonia</option>
                <option value="New Zealand">New Zealand</option>
                <option value="Nicaragua">Nicaragua</option>
                <option value="Niger">Niger</option>
                <option value="Nigeria">Nigeria</option>
                <option value="Niue">Niue</option>
                <option value="Norfolk Island">Norfolk Island</option>
                <option value="Northern Mariana Islands">Northern Mariana Islands</option>
                <option value="Norway">Norway</option>
                <option value="Oman">Oman</option>
                <option value="Pakistan">Pakistan</option>
                <option value="Palau">Palau</option>
                <option value="Palestinian Territory, Occupied">Palestinian Territory, Occupied</option>
                <option value="Panama">Panama</option>
                <option value="Papua New Guinea">Papua New Guinea</option>
                <option value="Paraguay">Paraguay</option>
                <option value="Peru">Peru</option>
                <option value="Philippines">Philippines</option>
                <option value="Pitcairn">Pitcairn</option>
                <option value="Poland">Poland</option>
                <option value="Portugal">Portugal</option>
                <option value="Puerto Rico">Puerto Rico</option>
                <option value="Qatar">Qatar</option>
                <option value="Reunion">Reunion</option>
                <option value="Romania">Romania</option>
                <option value="Russian Federation">Russian Federation</option>
                <option value="Rwanda">Rwanda</option>
                <option value="Saint Helena">Saint Helena</option>
                <option value="Saint Kitts and Nevis">Saint Kitts and Nevis</option>
                <option value="Saint Lucia">Saint Lucia</option>
                <option value="Saint Pierre and Miquelon">Saint Pierre and Miquelon</option>
                <option value="Saint Vincent and The Grenadines">Saint Vincent and The Grenadines</option>
                <option value="Samoa">Samoa</option>
                <option value="San Marino">San Marino</option>
                <option value="Sao Tome and Principe">Sao Tome and Principe</option>
                <option value="Saudi Arabia">Saudi Arabia</option>
                <option value="Senegal">Senegal</option>
                <option value="Serbia">Serbia</option>
                <option value="Seychelles">Seychelles</option>
                <option value="Sierra Leone">Sierra Leone</option>
                <option value="Singapore">Singapore</option>
                <option value="Slovakia">Slovakia</option>
                <option value="Slovenia">Slovenia</option>
                <option value="Solomon Islands">Solomon Islands</option>
                <option value="Somalia">Somalia</option>
                <option value="South Africa">South Africa</option>
                <option value="South Georgia and The South Sandwich Islands">South Georgia and The South Sandwich
                    Islands
                </option>
                <option value="Spain">Spain</option>
                <option value="Sri Lanka">Sri Lanka</option>
                <option value="Sudan">Sudan</option>
                <option value="Suriname">Suriname</option>
                <option value="Svalbard and Jan Mayen">Svalbard and Jan Mayen</option>
                <option value="Swaziland">Swaziland</option>
                <option value="Sweden">Sweden</option>
                <option value="Switzerland">Switzerland</option>
                <option value="Syrian Arab Republic">Syrian Arab Republic</option>
                <option value="Taiwan, Province of China">Taiwan, Province of China</option>
                <option value="Tajikistan">Tajikistan</option>
                <option value="Tanzania, United Republic of">Tanzania, United Republic of</option>
                <option value="Thailand">Thailand</option>
                <option value="Timor-leste">Timor-leste</option>
                <option value="Togo">Togo</option>
                <option value="Tokelau">Tokelau</option>
                <option value="Tonga">Tonga</option>
                <option value="Trinidad and Tobago">Trinidad and Tobago</option>
                <option value="Tunisia">Tunisia</option>
                <option value="Turkey">Turkey</option>
                <option value="Turkmenistan">Turkmenistan</option>
                <option value="Turks and Caicos Islands">Turks and Caicos Islands</option>
                <option value="Tuvalu">Tuvalu</option>
                <option value="Uganda">Uganda</option>
                <option value="Ukraine">Ukraine</option>
                <option value="United Arab Emirates">United Arab Emirates</option>
                <option value="United Kingdom">United Kingdom</option>
                <option value="United States">United States</option>
                <option value="United States Minor Outlying Islands">United States Minor Outlying Islands</option>
                <option value="Uruguay">Uruguay</option>
                <option value="Uzbekistan">Uzbekistan</option>
                <option value="Vanuatu">Vanuatu</option>
                <option value="Venezuela">Venezuela</option>
                <option value="Viet Nam">Viet Nam</option>
                <option value="Virgin Islands, British">Virgin Islands, British</option>
                <option value="Virgin Islands, U.S.">Virgin Islands, U.S.</option>
                <option value="Wallis and Futuna">Wallis and Futuna</option>
                <option value="Western Sahara">Western Sahara</option>
                <option value="Yemen">Yemen</option>
                <option value="Zambia">Zambia</option>
                <option value="Zimbabwe">Zimbabwe</option>"""