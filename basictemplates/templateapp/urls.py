from django.conf.urls import url
from templateapp import views

app_name = 'templateapp'

urlpatterns = [
    url(r'^relative_url/$', views.relative_url, name = 'relative_url'),
    url(r'^others/$', views.others, name = 'others'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^user_login/$', views.user_login, name = 'user_login')
]
