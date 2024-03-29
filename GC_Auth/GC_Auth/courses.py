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


class course_methods:

    def getCourseName(course_id):
        return database.child("Courses").child(course_id).child("CourseName").get().val()

    def getCourseTopics(course_id):
        return database.child("Courses").child(course_id).child("Topic").shallow().get().val()

    def getCoursesTopicsString(course_id):
        # gets all topics and puts them into one string
        topics = database.child("Courses").child(course_id).child("Topic").shallow().get().val()

        if topics is not None:
            for topic in topics:
                return "|" + topic + "|"
        else:
            topics_string = "No Topics"

        return topics_string

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

        if num_rec >= 200 and num_rec < 500:
            return "Well Rated"

        if num_rec >= 500:
            return "Highly Rated"

    def getCourseNumRecommendations(course_id):
        return database.child("Courses").child(course_id).child("NumRecommendations").get().val()

    def getCourseURL(course_id):
        return database.child("Courses").child(course_id).child("CourseURL").get().val()

    def getAllCoursesList(uid):
        return database.child("Courses").shallow().get().val()

    def getCourseHearted(uid, course_id):
        return database.child("Users").child(uid).child("Courses").child(course_id).child('hearted').get().val()

    def getCourseDescription(course_id):
        return database.child("Courses").child(course_id).child("Description").get().val()

    def getCourseStartDate(course_id):
        return database.child("Courses").child(course_id).child("StartDate").get().val()

    def getCourseRegClosesDate(course_id):
        return database.child("Courses").child(course_id).child("RegClosesDate").get().val()

    def getCourseLength(course_id):
        return database.child("Courses").child(course_id).child("Length").get().val()

    def getCourseEffort(course_id):
        return database.child("Courses").child(course_id).child("Effort").get().val()

    def getCourseDetailsList(uid, courses_id_list):
        course_image = []
        course_name = []
        course_description = []
        course_start = []
        course_topics = []
        course_rating = []
        reg_closes = []
        course_length = []
        course_effort = []
        course_url = []
        course_id = []

        if courses_id_list is not None:
            for id in courses_id_list:
                course_id.append(id)
                course_name.append(course_methods.getCourseName(id))
                course_image.append(course_methods.getCoursePicture(id))
                course_url.append(course_methods.getCourseURL(id))
                course_description.append(course_methods.getCourseDescription(id))
                course_start.append(course_methods.getCourseStartDate(id))
                course_topics.append(course_methods.getCoursesTopicsString(id))
                course_rating.append(course_methods.getCourseRecommended(id))
                reg_closes.append(course_methods.getCourseRegClosesDate(id))
                course_length.append(course_methods.getCourseLength(id))
                course_effort.append(course_methods.getCourseEffort(id))


        # return a combination of all lists
        combined_list = zip(course_id, course_image, course_name, course_description, course_start, course_topics, course_rating, reg_closes, course_length, course_effort, course_url)
        return combined_list

    def getCoursesInfoList(uid, courses_id_list):
        # get data from each course for the user and add them to separate arrays
        course_names = []
        course_pictures = []
        course_recommendations = []
        course_urls = []
        course_uni_pics = []
        courses_ids = []
        course_topics = []
        course_uni = []
        course_hearted = []

        if courses_id_list is not None:
            for id in courses_id_list:
                try:
                    course_names.append(course_methods.getCourseName(id))
                    course_pictures.append(course_methods.getCoursePicture(id))
                    course_recommendations.append(course_methods.getCourseRecommended(id))
                    course_urls.append(course_methods.getCourseURL(id))
                    course_uni_pics.append(course_methods.getCourseUniPic(id))
                    courses_ids.append(id)
                    course_topics.append(course_methods.getCoursesTopicsString(id))
                    course_uni.append(course_methods.getCourseUniversity(id))
                    course_hearted.append(course_methods.getCourseHearted(uid, id))
                except:
                    print("")

        # return a combination of all lists
        combined_list = zip(course_names, course_pictures, course_recommendations, course_urls, course_uni_pics,
                            courses_ids, course_topics, course_uni, course_hearted)
        return combined_list

    def getCourseSuggestions(uid, num_returns, the_user):
            # returns a combines list of courses that match the user's interests
            results_count = 0  # how many results were found thus far
            results = []

            all_courses_list = database.child(
                "Courses").shallow().get().val()  # list of all courses in the db - only their id's
            all_user_courses = database.child("Users").child(uid).child(
                "Courses").shallow().get().val()  # list of all courses that this user has done
            courses_list = course_methods.removeValuesFromList(all_user_courses,
                                                all_courses_list)  # remove the courses that the user has already done from the list of all courses

            if courses_list is not None:
                for compare_course_id in courses_list:  # loop through each course in the list
                    if results_count == num_returns:  # if we have the requested number of ids, stop searching
                        break
                    else:  # get the list of topics for each course
                        compare_courses_topics = database.child("Courses").child(compare_course_id).child(
                            "Topic").shallow().get().val()
                        if course_methods.compareLists(compare_courses_topics,
                                        the_user.topicsList):  # if there are matching topics between the user and the course
                            results.append(compare_course_id)  # add the course to the list of suggestions
                            results_count += 1  # increment number fo results by 1
            else:
                results = []

            return results

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


# UPDATE Methods

    def updateCourseNumRecommendations(course_id, num_rec):
        database.child("Courses").child(course_id).update({'NumRecommendations': num_rec})
