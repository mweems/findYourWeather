
from django.conf.urls import url, include
from django.contrib import admin
from weather import views 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
	url(r'^login', views.login, name='login' ),
]
