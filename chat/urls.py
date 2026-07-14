from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from .views import register , login , index,search,user_logout,add_user_to_chatroom,chatroom

urlpatterns = [
    path('register/' , register , name = 'register' ) ,
    path('login/' ,  login, name= 'login') ,
    path('' , index ,  name  = 'index') ,
    path('search/' , search , name = 'search_users' ) ,
    path('logout/' , user_logout , name  = 'logout'),
    path('createroom/<int:user_id>/' ,add_user_to_chatroom , name  = 'create_chat_room'),
    path('chatroom/<int:room_id>/' , chatroom , name  = 'chatroom')
]

# ************* FOR IMAGE UPLOAD ************