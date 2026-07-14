from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    #FK to user
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to = 'profile_images/',blank=True,null=True)

    def __str__(self) :  # for admin page
        return self.name 

class ChatRoom(models.Model) : 
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User,related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add = True) # to add the current date
    def __str__(self):
        return self.name
    

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name='message')
    sender = models.ForeignKey(User , on_delete = models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ['timestamp']