
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from weather import views
from weatherApp import settings 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^weather/$', views.weather, name='weather'),
    url(r'^delete/(?P<city>(\w+))/$', views.delete, name='delete'),
    url(r'^set_current/(?P<city>([\w\ ]+))/$', views.set_current, name='set_current'),
	url(r'^signup', views.signup, name='signup' ),
	url(r'^login/$', auth_views.login, {'template_name': 'login.html'},name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
]
