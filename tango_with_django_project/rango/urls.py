from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^about/', views.about, name='about'),
        url(r'^(?P<sport_name_url>\w+)/$', views.sport, name='sport'),  # New!)
        url(r'^\w+/(?P<team_name_url>\w+)/$', views.team, name='team'),  # New!)
        url(r'^\w+/(?P<set_name_url>\w+)/$', views.set, name='set'),  # New!)
        url(r'^\w+/\w+/(?P<player_name_url>\w+)/$', views.player, name='player'),  # New!)
        )