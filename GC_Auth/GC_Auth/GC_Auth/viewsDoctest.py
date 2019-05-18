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


class ViewsTest(unittest.TestCase):

    def test_get_username(self):
        self.assertEqual(GC_Auth.views.getUsername(user), "Kimone Premlall")

    def test_get_country(self):
        self.assertEqual(GC_Auth.views.getCountry(user), "South Africa")

    def test_get_num_connections(self):
        self.assertEqual(GC_Auth.views.getNumConnecions("", user), 1)

    def test_get_bio(self):
        self.assertEqual(GC_Auth.views.getBio("", user), "Kimone is my name")

    def test_get_num_forums(self):
        self.assertEqual(GC_Auth.views.getNumForums("", user), 1)

    def test_get_profile_pic(self):
        self.assertEqual(GC_Auth.views.getProfilePic("", user), "https://i.pinimg.com/originals/05/63/cd/0563cd1937bea536929a85e33fa6bfbe.jpg")

    def test_get_background_pic(self):
        self.assertEqual(GC_Auth.views.getBackgroundPic("", user), "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/FML_Logo.svg/250px-FML_Logo.svg.png")

    def test_get_bio_privacy(self):
        self.assertEqual(GC_Auth.views.getBioPrivacy(user), "False")

    def test_get_connection_privacy(self):
        self.assertEqual(GC_Auth.views.getConnectionPrivacy(user), "False")

    def test_get_country_privacy(self):
        self.assertEqual(GC_Auth.views.getConnectionPrivacy(user), "False")

    def test_get_name_privacy(self):
        self.assertEqual(GC_Auth.views.getNamePrivacy(user), "False")

    def test_get_pic_privacy(self):
        self.assertEqual(GC_Auth.views.getPicPrivacy(user), "False")

    def test_update_username(self):
        newEntry = "Kimone Premlall"
        GC_Auth.views.updateUsername(user, newEntry)
        self.assertEqual(GC_Auth.views.getUsername(user), newEntry)

    def test_update_bio(self):
        newEntry = "Kimone is my name"
        GC_Auth.views.updateBio(user, newEntry)
        self.assertEqual(GC_Auth.views.getBio("", user), newEntry)

    def test_update_country(self):
        newEntry = "South Africa"
        GC_Auth.views.updateCountry(user, newEntry)
        self.assertEqual(GC_Auth.views.getCountry(user), newEntry)

    def test_update_profile_pic(self):
        newEntry = "https://i.pinimg.com/originals/05/63/cd/0563cd1937bea536929a85e33fa6bfbe.jpg"
        GC_Auth.views.updateProfilePic(user, newEntry)
        self.assertEqual(GC_Auth.views.getProfilePic("", user), newEntry)

    def test_update_background_pic(self):
        newEntry =  "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/FML_Logo.svg/250px-FML_Logo.svg.png"
        GC_Auth.views.updateBackgroundPic(user, newEntry)
        self.assertEqual(GC_Auth.views.getBackgroundPic("", user), newEntry)

    def test_update_bio_privacy(self):
        newEntry = "False"
        GC_Auth.views.updateBioPrivacy(user, newEntry)
        self.assertEqual(GC_Auth.views.getBioPrivacy(user), newEntry)

    def test_update_name_privacy(self):
        newEntry = "False"
        GC_Auth.views.updateNamePrivacy(user, newEntry)
        self.assertEqual(GC_Auth.views.getNamePrivacy(user), newEntry)

    def test_update_country_privacy(self):
        newEntry = "False"
        GC_Auth.views.updateCountryPrivacy(user, newEntry)
        self.assertEqual(GC_Auth.views.getCountryPrivacy(user), newEntry)

    def test_update_connection_privacy(self):
        newEntry = "False"
        GC_Auth.views.updateConnectionPrivacy(user, newEntry)
        self.assertEqual(GC_Auth.views.getConnectionPrivacy(user), newEntry)

    def test_update_pic_privacy(self):
        newEntry = "False"
        GC_Auth.views.updatePicPrivacy(user, newEntry)
        self.assertEqual(GC_Auth.views.getPicPrivacy(user), newEntry)

    def test_get_courses_list(self):
        uid = "xxQe6gmBPGcj35WLLFw96BG7fkl1"
        GC_Auth.views.getCoursesInfoList(GC_Auth.views.getCoursesList(uid))


if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)

