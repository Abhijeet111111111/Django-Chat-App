from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from .models import UserInfo, ChatRoom, Message
from django.contrib.auth import login as auth_login ,authenticate , logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def register(request):
    if request.method == 'POST' :
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            phone = request.POST['phone']
            image = request.FILES.get('image')
            name = request.POST['name']

            if User.objects.filter(username = username).exists() :
                messages.error(request,"Username already taken")
                return redirect('register')

            user = User.objects.create_user(username=username,password=password)
            user_info = UserInfo.objects.create(user = user , name = name , email = email , phone = phone , image = image)
            # first save user then user info , since it has FK , so it depends upon USer
            user.save()
            user_info.save()
            auth_login(request,user=user)
            messages.success(request,"Register succssful")
            return redirect('index')
    return render(request, 'chat/register.html',{"user" : {}})

def login(request):
    if request.method == 'POST' :
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request,username = username , password = password)

            if user :
                    auth_login(request,user = user) 
                    return redirect('index')
            else :
                messages.error(request,"Invalid username or Password")
            
    return render(request,"chat/login.html",{"user" : {}})


@login_required
def index(request):
    user = request.user
    chatrooms = ChatRoom.objects.filter(participants=user).distinct()

    # Add other participant info to each room object
    # for room in chatrooms:
    #     other = room.participants.exclude(id=user.id).first()
    #     room.other_user = other  # dynamically attach for template use

    return render(request, 'chat/index.html', {'chatrooms': chatrooms})

@login_required
def search(request):
    query = request.GET.get('q', '')
    users = []

    if query:
        users = User.objects.filter(
            Q(username=query) |
            Q(email=query) |
            Q(userinfo__name__icontains=query) |
            Q(userinfo__email__icontains=query)
        ).exclude(id=request.user.id).distinct()

    return render(request, 'chat/search.html', {'query': query, 'users': users})

@login_required
def chatroom(request ,  room_id) :
    room  =  get_object_or_404(ChatRoom , id =  room_id)

    if request.user not in room.participants.all() :
        return redirect('index')
    messages = Message.objects.filter(chatroom=room)
    print(messages)
    return render(request ,  'chat/chatroom.html' ,  {
        'room' : room , 'messages' : messages
    })

@login_required
def add_user_to_chatroom(request  , user_id) :
    reciver  =  User.objects.get(id =  user_id)
    sender = request.user

    chatroom = ChatRoom.objects.filter(participants = sender).filter(participants = reciver).first()

    if chatroom is None :
        name  = f"{reciver.username}-{sender.username}"
        chatroom  = ChatRoom.objects.create(name  = name)
        chatroom.participants.add(reciver ,  sender)
        chatroom.save()

    return redirect('chatroom' ,  room_id =  chatroom.id)

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  # Replace 'login' with your login page URL name