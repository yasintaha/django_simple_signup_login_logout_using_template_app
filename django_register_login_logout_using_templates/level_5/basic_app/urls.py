from django.conf.urls import url
from django.urls import path
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    path('user_login/',views.login_user,name='user_login')
    
] 