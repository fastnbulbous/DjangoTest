from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^about/', views.about, name='about'),
        url(r'^sport/(?P<sport_name_url>\w+)/$', views.sport, name='sport'),)  # New!)