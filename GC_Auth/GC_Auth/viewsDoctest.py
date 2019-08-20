import unittest
import sys
import doctest
from django.http import HttpResponseRedirect
from django.shortcuts import render
import pyrebase
from django.contrib import  auth
import GC_Auth.views
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

email = 'prmkim003@myuct.ac.za'
password = '123456'
uid = "xxQe6gmBPGcj35WLLFw96BG7fkl1"
user = authe.sign_in_with_email_and_password(email, password)
forum_id = "CTIB01"
course_id = "HVD_FinTech"


class ViewsTest(unittest.TestCase):

    # user tests
    def test_get_username(self):
        self.assertEqual(GC_Auth.views.user_methods.getUsername(uid), "Kimone Premlall")

    def test_get_country(self):
        self.assertEqual(GC_Auth.views.user_methods.getCountry(uid), "SouthAfrica")

    def test_get_num_connections(self):
        self.assertEqual(GC_Auth.views.user_methods.getNumConnecions(uid), 1)

    def test_get_bio(self):
        self.assertEqual(GC_Auth.views.user_methods.getBio(uid), "Kimone is my name")

    def test_get_num_forums(self):
        self.assertEqual(GC_Auth.views.user_methods.getNumForums(uid), 1)

    def test_get_profile_pic(self):
        profilePic = "https://i.pinimg.com/originals/05/63/cd/0563cd1937bea536929a85e33fa6bfbe.jpg"
        self.assertEqual(GC_Auth.views.user_methods.getProfilePic(uid), profilePic)

    def test_get_bio_privacy(self):
        self.assertEqual(GC_Auth.views.user_methods.getBioPrivacy(uid), "False")

    def test_get_connection_privacy(self):
        self.assertEqual(GC_Auth.views.user_methods.getConnectionPrivacy(uid), "False")

    def test_get_country_privacy(self):
        self.assertEqual(GC_Auth.views.user_methods.getConnectionPrivacy(uid), "False")

    def test_get_pic_privacy(self):
        self.assertEqual(GC_Auth.views.user_methods.getPicPrivacy(uid), "False")

    def test_update_username(self):
        newEntry = "Kimone Premlall"
        GC_Auth.views.user_methods.updateUsername(uid, newEntry)
        self.assertEqual(newEntry, GC_Auth.views.user_methods.getUsername(uid))

    def test_update_country(self):
        newEntry = "SouthAfrica"
        GC_Auth.views.user_methods.updateCountry(uid, newEntry)
        self.assertEqual(newEntry, GC_Auth.views.user_methods.getCountry(uid))

    def test_update_bio(self):
        newEntry = "Kimone is my name"
        GC_Auth.views.user_methods.updateBio(uid, newEntry)
        self.assertEqual(newEntry, GC_Auth.views.user_methods.getBio(uid))

    def test_update_forums_privacy(self):
        newEntry = "False"
        GC_Auth.views.user_methods.updateForumsPrivacy(uid, newEntry)
        self.assertEqual(newEntry, GC_Auth.views.user_methods.getForumsPrivacy(uid))

    def test_update_courses_privacy(self):
        newEntry = "False"
        GC_Auth.views.user_methods.updateCoursesPrivacy(uid, newEntry)
        self.assertEqual(newEntry, GC_Auth.views.user_methods.getCoursesPrivacy(uid))

    # forum tests
    def test_get_forum_name(self):
        self.assertEqual("CT Investment Bankers", GC_Auth.views.forum_methods.getForumName(forum_id))

    def test_get_forum_num_participants(self):
        self.assertEqual(100, GC_Auth.views.forum_methods.getForumNumParticipants(forum_id))

    def test_get_forum_pic(self):
        self.assertEqual("https://firebasestorage.googleapis.com/v0/b/getconnected-9dac0.appspot.com/o/Forums%2Finvestment.jpeg?alt=media&token=5673334d-e757-4d05-9da4-d440bc7b7a38", GC_Auth.views.forum_methods.getForumPic(forum_id))

    def test_get_forum_creator(self):
        self.assertEqual("Winfreda", GC_Auth.views.forum_methods.getForumCreator(forum_id))

    def test_get_forum_description(self):
        self.assertEqual("Just a bunch of bankers talking about finance, sometimes we get drinks! Join & let's network.", GC_Auth.views.forum_methods.getForumDescription(forum_id))

    # courses tests
    def test_get_course_name(self):
        self.assertEqual("FinTech Online Short Course", GC_Auth.views.course_methods.getCourseName(course_id))

    def test_get_course_uni(self):
        self.assertEqual("Harvard University", GC_Auth.views.course_methods.getCourseUniversity(course_id))

    def test_get_course_num_recommendations(self):
        self.assertEqual(300, GC_Auth.views.course_methods.getCourseNumRecommendations(course_id))

    def test_get_course_uni_pic(self):
        self.assertEqual("https://alumni.harvard.edu/sites/default/files/slideshow/boston-slide-1.png", GC_Auth.views.course_methods.getCourseUniPic(course_id))

    def test_get_course_url(self):
        self.assertEqual("https://www.getsmarter.com/courses/us/harvard-fintech-online-short-course", GC_Auth.views.course_methods.getCourseURL(course_id))

    def test_get_course_pic(self):
        self.assertEqual("https://firebasestorage.googleapis.com/v0/b/getconnected-9dac0.appspot.com/o/Courses%2FHARVARD.png?alt=media&token=3d4f194d-caf2-4b9f-8cab-1fb9551435de", GC_Auth.views.course_methods.getCoursePicture(course_id))

    # array manipulation
    def test_remove_values_from_list(self):
        temp1 = ['a', 'b', 'c', 'd', 'e']
        temp2 = ['d', 'e']
        self.assertEqual(['a', 'b', 'c'], GC_Auth.views.connection_methods.removeValuesFromList(temp2, temp1))

    def test_remove_values_from_list_blank2(self):
        temp1 = ['a', 'b', 'c', 'd', 'e']
        temp2 = []
        self.assertEqual(['a', 'b', 'c', 'd', 'e'], GC_Auth.views.connection_methods.removeValuesFromList(temp2, temp1))

    def test_remove_values_from_list_blank1(self):
        temp1 = []
        temp2 = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual([], GC_Auth.views.connection_methods.removeValuesFromList(temp2, temp1))

    def test_remove_values_from_list(self):
        temp1 = ['a', 'b', 'c', 'd', 'e']
        temp2 = 'e'
        self.assertEqual(['a', 'b', 'c', 'd'], GC_Auth.views.connection_methods.removeValueFromList(temp2, temp1))

    def test_compare_list_equal(self):
        temp1 = ['a', 'b', 'c', 'd', 'e']
        temp2 = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(True, GC_Auth.views.connection_methods.compareLists(temp2, temp1))

    def test_compare_list_not_equal(self):
        temp1 = ['a', 'b', 'c', 'd', 'e']
        temp2 = ['a', 'b', 'd', 'e']
        self.assertEqual(True, GC_Auth.views.connection_methods.compareLists(temp2, temp1))

    def test_compare_list_blank2(self):
        temp1 = ['a', 'b', 'c', 'd', 'e']
        temp2 = []
        self.assertEqual(False, GC_Auth.views.connection_methods.compareLists(temp2, temp1))

    def test_compare_list_no_matching(self):
        temp1 = ['a', 'b', 'c', 'd', 'e']
        temp2 = ['f', 'g', 'h']
        self.assertEqual(False, GC_Auth.views.connection_methods.compareLists(temp2, temp1))


if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)

