from django.conf.urls import url
from . import views

urlpatterns = [
	    url(r'^$', views.index, name = 'logout'),
        url(r'^login$', views.login),
        url(r'^register$', views.register),
        url(r'^add_user$', views.add_user),
        url(r'^user_page$', views.user_page, name= 'dash'),
        url(r'^users$', views.users, name ='users'),
        url(r'^upload_file$', views.upload_file, name ='upload'),
        url(r'^(?P<id>\d+)/user_dashboard$', views.user_dashboard, name= 'userDash'),
        url(r'^(?P<id>\d+)/edit$', views.edit_user, name ='editProfile'),
        url(r'^update_user$', views.update_user),
        url(r'^update_password$', views.update_password)

	]
