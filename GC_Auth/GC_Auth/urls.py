"""cpanel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.urls import path, include




urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$',views.LogIn),
    url(r'^passwordReset/', views.passwordReset, name='Reset'),
    url(r'^postsign/',views.postsign),
    url(r'^logout/',views.logout,name="log"),
    url(r'^goBadges/', views.goBadges, name='goBadges'),
    url(r'^Settings/', views.goSettings, name='goSettings'),

    url(r'^goHelpUserProfile/', views.goHelpUserProfile, name='helpUserProfile'),
    url(r'^goIntroHelp/', views.goIntroHelp, name='introHelp'),
    url(r'^goAccountHelp/', views.goAccountHelp, name='accountHelp'),
    url(r'^goForumsOpen/', views.goForumsOpen, name='forumsopen'),
    url(r'^goSettings/', views.goSettings, name='settings'),
    url(r'^goContact/', views.goContact, name='contactus'),
    url(r'^goLogIn/', views.LogIn, name='login'),



    url(r'^home/', views.home, name="nav_home"),
    url(r'^networks/', views.networks, name="nav_networks"),
    url(r'^forums/', views.forums, name="nav_forums"),
    url(r'^courses/', views.courses, name="nav_courses"),
    url(r'^userprofile/', views.userprofile, name="userprofile")


]
