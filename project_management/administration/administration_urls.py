from django.conf.urls import url, include
from django.contrib import admin
# from .views import listUserf'

from administration import views
urlpatterns = [
               url(r'^login/$', views.login_page),
               url(r'^authenticate/$', views.authenticate_user),
               url(r'^main/$', views.main),
               url(r'^sprint/$', views.sprint),
               url(r'^sprint/add/$', views.add_sprint),
               url(r'^task/$', views.task),
               url(r'^task/add/$', views.add_task),
               url(r'^subtask/$', views.subtask),
               url(r'^subtask/add/$', views.add_subtask),
               url(r'^effort/$', views.effort_tracking),
               url(r'^effort/edit/(\d+)/$', views.edit_effort),
               url(r'^effort/edit/(\d+)/save/$', views.save_effort),
               url(r'^tracking/$', views.track_effort),
               url(r'^review/$', views.review),
               url(r'^review/add/$', views.add_review),
               url(r'^profile/$', views.profile),
               url(r'^profile/save/$', views.save_profile),
]
