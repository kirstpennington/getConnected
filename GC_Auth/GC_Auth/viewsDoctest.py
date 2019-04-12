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

    def test_updates(self):
        self.assertEqual(GC_Auth.views.getUsername(user), "Kimone Premlall")

    def test_get_country(self):
        self.assertEqual(GC_Auth.views.getCountry(user), "South Africa")

    def test_get_num_connections(self):
        self.assertEqual(GC_Auth.views.getNumConnecions("", user), 1)

    def test_get_bio(self):
        self.assertEqual(GC_Auth.views.getBio("", user), "Kimone is my name")

    def test_get_num_forums(self):
        self.assertEqual(GC_Auth.views.getNumForums("", user), 3)


if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)

