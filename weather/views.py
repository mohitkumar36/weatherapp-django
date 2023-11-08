from django.shortcuts import render, redirect
import json
import urllib.request
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from weather.models import Item, Review

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, email = email, password = password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password not the same')
            return redirect('register')
    else:
        return render(request, 'register.html')

@login_required(login_url="/login")
def index(request):
    if request.method == "POST":
        city = request.POST['city'].strip()
        tmp = ''
        for c in city.lower():
            if c == ' ' and tmp and tmp[-1] == '_':
                continue
            tmp += c

        city = tmp
        search_type = request.POST['search_type'].strip()
        

        try:
            if search_type == 'by_city':
                req = urllib.request.Request(
                            url='https://api.openbrewerydb.org/v1/breweries?by_city='+city, 
                            headers={'User-Agent': 'Mozilla/5.0'}
                        )
                webpage = urllib.request.urlopen(req).read()

                json_data = json.loads(webpage)

                data = {}
                for i, v in enumerate(json_data):
                    data[str(i)]=v


            elif search_type == 'by_name':
                req = urllib.request.Request(
                            url='https://api.openbrewerydb.org/v1/breweries?by_name='+city, 
                            headers={'User-Agent': 'Mozilla/5.0'}
                        )
                webpage = urllib.request.urlopen(req).read()

                json_data = json.loads(webpage)

                data = {}
                for i, v in enumerate(json_data):
                    data[str(i)]=v

            else:
                req = urllib.request.Request(
                            url='https://api.openbrewerydb.org/v1/breweries?by_type='+city, 
                            headers={'User-Agent': 'Mozilla/5.0'}
                        )
                webpage = urllib.request.urlopen(req).read()

                json_data = json.loads(webpage)

                data = {}
                for i, v in enumerate(json_data):
                    data[str(i)]=v


            
        except:
            data = {'0': {'city': 'City not found'}}
    else:
        data = {'city':''}
    return render(request, 'index.html', {'data':data})


def review(request, review):
    room_details = Item.objects.get(id_for=review)
    username = request.GET.get('username')

    messages = Review.objects.filter(id_for=review)
    # print("********"*3)
    # print(messages.values())

    return render(request, 'review.html', {
                    'username': username,
                   'id':review,
                   'room_details':room_details,
                   'messages':list(messages.values())
                   })


def check(request, id):
    room = id
    # username = "Mohit"
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    if Item.objects.filter(id_for=room).exists():
        return redirect('/' + room + '/?username='+username)
    
    new_item = Item.objects.create(id_for=room)
    new_item.save()
    return redirect('/' + room + '/?username='+username)

def send(request):
    message = request.POST['body']
    username = request.POST['username']
    room_id = request.POST['room_id']
    rate = request.POST['rate']
    # print("here")
    # print(message, username, room_id, rate)
    new_message = Review.objects.create(body=message, user=username, id_for=room_id, rating=rate)
    new_message.save()
    return HttpResponse("Message sent")

# def getMessages(request, room):
#     room_details = Item.objects.get(id_for=room)

#     messages = Review.objects.filter(room=room_details.id)
#     return JsonResponse({'messages':list(messages.values())})