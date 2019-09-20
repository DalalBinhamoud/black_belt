from django.conf.urls import url
from . import views

urlpatterns = [
	    url(r'^$', views.index, name = 'logout'),
        url(r'^login$', views.login),
        url(r'^register$', views.register),
        url(r'^add_user$', views.add_user),
        url(r'^user_page$', views.user_page, name= 'dash'),
        url(r'^users$', views.users, name ='users')
	]