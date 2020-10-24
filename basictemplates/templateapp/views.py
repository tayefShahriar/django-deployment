from django.shortcuts import render
from templateapp.forms import UserForm, UserProfileInfo
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def index(response):
    return render(response, 'templateapp/index.html')

@login_required
def special(response):
    return HttpResponse("You are logged in, Nice!")

@login_required
def user_logout(response):
    logout(response)
    return HttpResponseRedirect(reverse('index'))

def others(response):
    return render(response, 'templateapp/others.html')

def relative_url(response):
    return render(response, 'templateapp/relative_url.html')
def register(response):

    registered = False

    if response.method == "POST":

        user_form = UserForm(data = response.POST)
        profile_form = UserProfileInfo(data = response.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            if 'profile_pic' in response.FILES:
                profile.profile_pic = response.FILES['profile_pic']
            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfo()

    return render(response, 'templateapp/registration.html',
                            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(response):

    if response.method == 'POST':
        username = response.POST.get('username')
        password = response.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(response, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and Password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:

        return render(response, 'templateapp/login.html', {})
