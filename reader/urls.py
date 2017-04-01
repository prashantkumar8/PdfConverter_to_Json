from django.conf.urls import url

from . import views

app_name = 'reader'
urlpatterns = [
	url(r'^list/', views.get_data, name='mainfile'),
	url(r'^main/', views.main, name='mainfile'),
	url(r'^upload/', views.upload, name='uploadfile'),
]