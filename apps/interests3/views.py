from django.shortcuts import render, redirect
from .models import User, Interest
from django.contrib import messages
from django.db.models import Count

from .models import User, Interest
# Create your views here.
def index(request):
    users = User.objects.all()
    for user in users:
        print user.username
    if 'messages' in request.session:
        context={
        'messages': request.session['messages']
        }
        del request.session['messages']
    else:
        context = {
        'messages': [],
        'users': users
        }
    return render(request, 'interests3/index.html')

def register(request):
    #print request.POST
    if request.method == 'POST':
        messages = User.objects.register(request.POST)
        #Above line might be postData
    if not messages:
        print "No messages! Success!"
        # fetch user id and name via email
        user_list = User.objects.all().filter(username=request.POST['username'])
        request.session['id'] = user_list[0].id
        request.session['name'] = user_list[0].first_name
        request.session['username'] = user_list[0].username
        return redirect('/add')
    else:
        request.session['messages'] = messages
        print messages
    return redirect('/')

def login(request):
    users = User.objects.all()
    # postData = {
    #     'username': request.POST['username'],
    #     'password': request.POST['password'],
    # }
    if request.method == 'POST':
        messages = User.objects.login(request.POST)
    if not messages:
        print "No messages! Success!"
        user_list = User.objects.all().filter(username=request.POST['username'])
        request.session['id'] = user_list[0].id
        request.session['name'] = user_list[0].first_name
        return redirect('/add')
    else:
        request.session['messages'] = messages
        return redirect('/')

def add(request):
    context ={
        'interests': Interest.objects.all()
    }

    return render(request, 'interests3/add.html', context)

def users(request):
    users = User.objects.all()
    interests = Interest.objects.all()
    context={
        'users': User.objects.all()
    }
    postData = {
        'interests': Interest.objects.all(),
    }
    return render(request, 'interests3/users.html', context)

def show(request, id):
    user = User.objects.get(id=id)
    users_interests = Interest.objects.get(id=id)
    interest_id = Interest.objects.get(id=id)
    interests = user.user_interests.all()
    all_interests = Interest.objects.all()
    # interest_list = Interest.objects.all().filter(user_interests__username=request.POST['username'])
    context = {
        'users_interests': users_interests,
        'interests': interests,
        'id': id,
        'interest_id': interest_id,
        'user': user
    }
    # print interest_list
    print "User: ", user
    print "Interests: ", interests
    print "Users Interests", users_interests
    print "Interest ID", interest_id
    return render(request, 'interests3/show.html', context)

def add_interest(request):
    user = User.objects.get(id=request.session['id'])
    interest = Interest.objects.filter(interest=request.POST['interest'])
    if not interest:
        interest = Interest.objects.create(interest=request.POST['interest'])
    else:
        interest = interest[0]
    print interest
    add_interest = interest.users.add(user)
    # print interest
    return redirect('/users')
