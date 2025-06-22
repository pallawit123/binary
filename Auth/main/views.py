# from django.shortcuts import render, redirect

# # Create your views here.
# def index(request):
#     return render(request, "main/index.html")


# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.contrib.auth.password_validation import validate_password
# import re  # Import the regular expression module

# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
# # from .models import User
# from django.contrib import messages


# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         # Check if passwords match
#         if password == confirm_password:
#             try:
#                 # Check if the email ends with @gmail.com
#                 if not email.endswith('@gmail.com'):
#                     messages.error(request, 'Please enter a valid Gmail address!!!')
#                     return redirect('register')

#                 # Check if username or email already exists
#                 if User.objects.filter(username=username).exists():
#                     messages.error(request, 'Username already exists!!!')
#                     return redirect('register')
                
#                 elif User.objects.filter(email=email).exists():
#                     messages.error(request, 'Email already exists!!!')
#                     return redirect('register')

#                 # Password strength checks
#                 # if len(password) < 8:
#                 #     messages.error(request, 'Password must be at least 8 characters long!!!')
#                 #     return redirect('register')
#                 # elif not re.search(r'[A-Z]', password):
#                 #     messages.error(request, 'Password must contain at least one uppercase letter!!!')
#                 #     return redirect('register')
#                 # elif not re.search(r'[0-9]', password):
#                 #     messages.error(request, 'Password must contain at least one numeric digit!!!')
#                 #     return redirect('register')
#                 # elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
#                 #     messages.error(request, 'Password must contain at least one special character!!!')
#                 #     return redirect('register')
#                 # elif username.lower() in password.lower():
#                 #     messages.error(request, 'Password must not contain the username!!!')

#                 # Validate password strength using Django's built-in validation
#                 validate_password(password)

#                 # Create the user
#                 User.objects.create_user(
#                     username=username,
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=email,
#                     password=password
#                 )
#                 # Display a thank you message with the username
#                 messages.success(request, f'Thank you for registering, {username}!!!')
#                 return redirect('log_in')

#             except ValidationError as e:
#                 for error in e.messages:
#                     messages.error(request, error)
#                 return redirect('register')
#         else:
#             messages.error(request, 'Passwords do not match!!!')
#             return redirect('register')

#     return render(request, 'auth/register.html')
#     # return render(request, 'sam/register.html')

# #  by specifying return redirect('page_name'), we're also specify where the message will appear.

# def log_in(request):
#     if request.method=="POST":
#         username=request.POST['username']
#         password=request.POST['password']
#         remember_me = request.POST.get('remember_me') # T or F

#         if not User.objects.filter(username=username):
#             messages.error(request,"Username does not exist")
#             return redirect('log_in')
#         else:
#             user=authenticate(username=username,password=password)
#             if user is not None:
#                 login(request,user)
#                 if remember_me:
#                     request.session.set_expiry(592200) # for 7 days 
#                 else:
#                     request.session.set_expiry(0)
#                 messages.success(request,"login successful")
#                 return redirect('index')
#             else:
#                 messages.error(request,"Incorrect Password")
#                 return redirect('log_in')
#     return render(request,'auth/login.html')

# def log_out(request):
#     logout(request)
#     return redirect('log_in')
    


# @login_required(login_url='log_in')
# def change_password(request):
#     form=PasswordChangeForm(user=request.user)
#     if request.method=='POST':
#         form=PasswordChangeForm(user=request.user,data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('log_in')      
    
#     return render(request,'auth/change_password.html',{'form':form})

# @login_required
# def user_profile(request):
#     return render(request, 'auth/user_profile.html')
















from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re  # Import the regular expression module

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib import messages

from .models import *


# _____________________________________________________________________________________________________________

def index(request):
    return render(request, "main/index.html")

@login_required(login_url='log_in')
def community(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        visit_date = request.POST.get('visit_date')
        location = request.POST.get('location')
        image = request.FILES.get('images')

        experience = TravelExperience(
            title=title,
            content=content,
            visit_date=visit_date,
            location=location,
            images=image,
            author=request.user
        )
        experience.save()
        return redirect('community')
    
    context = {
    'experiences': TravelExperience.objects.all().order_by('-created_at'),
    }


    return render(request, 'main/community.html', context)


@login_required(login_url='log_in')
def contribution(request):
    sites = HeritageSite.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        site_id = request.POST.get('associated_site')
        media = request.FILES.get('media')
        source = request.POST.get('source')
        verified = request.POST.get('verified') == 'on'

        site = HeritageSite.objects.get(id=site_id) if site_id else None

        Contribution.objects.create(
            title=title,
            content=content,
            associated_site=site,
            media=media,
            source=source,
            verified=verified,
            contributor=request.user
        )
        return redirect('contribution')
    
    contributions = Contribution.objects.order_by('-created_at') 

    return render(request, 'main/contribution.html', {'sites': sites,  'contributions': contributions})

#___________________________authentication starts here____________________________________________________
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password == confirm_password:
            try:
                # Check if the email ends with @gmail.com
                if not email.endswith('@gmail.com'):
                    messages.error(request, 'Please enter a valid Gmail address!!!')
                    return redirect('register')

                # Check if username or email already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists!!!')
                    return redirect('register')
                
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!!!')
                    return redirect('register')

                # Password strength checks
                # if len(password) < 8:
                #     messages.error(request, 'Password must be at least 8 characters long!!!')
                #     return redirect('register')
                # elif not re.search(r'[A-Z]', password):
                #     messages.error(request, 'Password must contain at least one uppercase letter!!!')
                #     return redirect('register')
                # elif not re.search(r'[0-9]', password):
                #     messages.error(request, 'Password must contain at least one numeric digit!!!')
                #     return redirect('register')
                # elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                #     messages.error(request, 'Password must contain at least one special character!!!')
                #     return redirect('register')
                # elif username.lower() in password.lower():
                #     messages.error(request, 'Password must not contain the username!!!')

                # Validate password strength using Django's built-in validation
                validate_password(password)

                # Create the user
                User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                # Display a thank you message with the username
                messages.success(request, f'Thank you for registering, {username}!!!')
                return redirect('log_in')

            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
                return redirect('register')
        else:
            messages.error(request, 'Passwords do not match!!!')
            return redirect('register')

    return render(request, 'sam/register.html')
    # return render(request, 'sam/register.html')

#  by specifying return redirect('page_name'), we're also specify where the message will appear.

def log_in(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        remember_me = request.POST.get('remember_me') # T or F

        if not User.objects.filter(username=username):
            messages.error(request,"Username does not exist")
            return redirect('log_in')
        else:
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if remember_me:
                    request.session.set_expiry(592200) # for 7 days 
                else:
                    request.session.set_expiry(0)
                messages.success(request,"login successful")
                return redirect('index')
            else:
                messages.error(request,"Incorrect Password")
                return redirect('log_in')
    return render(request,'sam/login.html')

def log_out(request):
    logout(request)
    return redirect('log_in')
    


@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')      
    
    return render(request,'sam/change_password.html',{'form':form})

@login_required
def user_profile(request):
    return render(request, 'auth/user_profile.html')

#___________________________authentication ends here____________________________________________________



# _________________________________food__________________________________________________________________

def ingredient_shop(request,id):
    data=Ingredient.objects.get(id=id)
    dd=Shop.objects.filter(ingredients=data)
    d = OnlineShop.objects.filter(ingredient=data)
    return render(request,'food/ingredient_shop.html',{'data':data,'shops':dd,'online_shops':d})

def recipe(request,id):
    food=Food.objects.get(id=id)
    data=Recipe.objects.get(name=food)
    return render(request,'food/recipe.html',{'recipe':data})

def historical_significance(request,id):
    food=Food.objects.get(id=id)
    data=Historical_Significance.objects.get(name=food)
    return render(request,'food/historical_significance.html',{'data':data})

def listoffood(request):
    data=Food.objects.all()
    return render(request,'food/listoffood.html',{'data':data})

def tutorial(request,id):
    food=Food.objects.get(id=id)
    return render(request,'food/video_tutorial.html',{'food':food})

def online_buying(request,id):
    food=Food.objects.get(id=id)
    data=OnlineBuying.objects.filter(name=food)
    return render(request,'food/online_buying.html',{'data':data,'food':food})

def restaurant(request,id):
    food=Food.objects.get(id=id)
    data=Restaurant.objects.filter(food=food)
    return render(request,'food/restaurant.html',{'data':data})


# _____________________________________________sites__________________________________________________________

def listofsites(request):
    sites=Sites.objects.all()
    return render(request,'sites/listofsites.html',{'sites':sites})

def site_detail(request, id):
    
    site = Sites.objects.get(id=id)
        
    context = {
            'site': site,
            'data': {
                'description': site.description,
                'history': site.history,
                'cultural_significance': site.cultural_significance
            }
        }
        
    return render(request, 'sites/site_detail.html', context)






from .utils import get_weather_data  # use .utils if you rename the file

import requests
from collections import defaultdict
from django.shortcuts import render

def weather_view(request):
    API_KEY = 'c9085be2ba255f1ff15d56c7dfb6c9a9'
    city = request.GET.get('city', '').strip()
    country = request.GET.get('country', '').strip().upper()

    weather = None
    forecast = []

    if city:
        # Build query for OpenWeatherMap
        query = city
        if country:
            query += f",{country}"

        # Fetch current weather
        current_url = f'https://api.openweathermap.org/data/2.5/weather?q={query}&appid={API_KEY}&units=metric'
        current_response = requests.get(current_url)
        current_data = current_response.json()

        if current_data.get('cod') == 200:
            weather = {
                'city': current_data['name'],
                'temperature': round(current_data['main']['temp'], 1),
                'description': current_data['weather'][0]['description'],
                'humidity': current_data['main']['humidity'],
                'wind': current_data['wind']['speed'],
                'icon_url': f"http://openweathermap.org/img/wn/{current_data['weather'][0]['icon']}@2x.png"
            }

        # Fetch 5-day forecast
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={query}&appid={API_KEY}&units=metric'
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        if forecast_data.get('cod') == '200':
            daily_data = defaultdict(list)
            for entry in forecast_data.get('list', []):
                date = entry['dt_txt'].split(' ')[0]
                daily_data[date].append(entry)

            for date, entries in list(daily_data.items())[:5]:
                temps = [e['main']['temp'] for e in entries]
                descriptions = [e['weather'][0]['description'] for e in entries]
                humidities = [e['main']['humidity'] for e in entries]
                winds = [e['wind']['speed'] for e in entries]
                icons = [e['weather'][0]['icon'] for e in entries]
                forecast.append({
                    'date': date,
                    'avg_temp': round(sum(temps) / len(temps), 1),
                    'description': descriptions[0],
                    'humidity': round(sum(humidities) / len(humidities)),
                    'wind': round(sum(winds) / len(winds), 1),
                    'icon_url': f"http://openweathermap.org/img/wn/{icons[0]}@2x.png"
                })

    return render(request, 'main/weather.html', {
        'weather': weather,
        'forecast': forecast,
        'city': city,
        'country': country
    })




from django.shortcuts import render
from .models import Event, Category, Tag

def events_view(request):
    events = Event.objects.all()
    featured_events = events.filter(is_featured=True)[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, "event/events.html", {
        "events": events,
        "featured_events": featured_events,
        "categories": categories,
        "tags": tags,
    })



def events_page(request):
    events = Event.objects.all()
    return render(request, 'event/events.html', {'events': events})
