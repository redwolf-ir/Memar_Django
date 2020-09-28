from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as auth_login
from .models import Profile, Passwordresetcodes
from django.http import HttpResponseRedirect
from .token import registration_token, password_reset_token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
import hashlib
import pytz
#------------------------------------------------------------------------------#


def register_view(request):
    # karbar dokme sabt nam ra click karde ast
    if 'requestcode' in request.POST:
        if User.objects.filter(email=request.POST['email']).exists():
            messages.error(
                request, 'This email address is already registered 😓.\
                     If it\'s yours, Retrieve your password from %s. </br> ' % '<a href="{% url \'password_reset\' %}">THIS LINK</a>')
            return redirect('register')
    # age karbar to database mojod nabashad
        if not User.objects.filter(username=request.POST['username']).exists():
            first_name = request.POST['first_name']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            password = make_password(request.POST['password'])
            user = User(
                email=email, username=username, password=password, first_name=first_name)
            user.is_active = False
            user.save()
            token = registration_token(username, email)
            userid = User.objects.get(email=request.POST['email']).id
            # send_mail(
            #     'ثبت نام در معمار دات کام',
            #     '<a href=\"{}?token={}&id={}\">\
# 		لینک رو به رو</a>'.format(request.build_absolute_uri
            #                    ('/register/'), token, userid),
            #     'info@memar.com',
            #     ['{}'.format(email)],
            #     fail_silently=False,
            # )
            messages.success(request, '<a href=\"{}?token={}&id={}\">\
				لینک رو به رو</a>'.format(request.build_absolute_uri
                              ('/register/'), token, userid))
            return redirect('register')
        else:
            messages.error(
                request, "That username is taken 😭. Try another!! ☹️")
            return redirect('register')

    # karbar email ersal shode ra click karde ast
    elif 'token' in request.GET and 'id' in request.GET:
        code = request.GET['token']
        userid = request.GET['id']
        thisuser = get_object_or_404(User, id=userid)
        token = registration_token(thisuser.username, thisuser.email)
        if code == token and thisuser.is_active == False:
            now = datetime.now()
            utc = pytz.UTC
            dt = now.replace(tzinfo=utc) - \
                thisuser.date_joined.replace(tzinfo=utc)
            dt = dt.days
            if dt < 1:
                thisuser.is_active = True
                thisuser.save()
                messages.success(
                    request, 'Registration successfully completed! 🥳')
                Profile.objects.get_or_create(user=request.user)
                return redirect('login')
            else:
                thisuser.delete()
                messages.error(
                    request, 'Your token has expired!!! 🤔 Request again (if you want 🤭)')
                return redirect('register')

        elif code == token and thisuser.is_active == True:
            messages.warning(
                request, 'This token has been used before! \
                    🥺 If you have lost your password, \
                    use %s' % '<a href="{% url \'password_reset\' %}" > PASSWORD RECOVERY </a>')
        else:
            messages.error(
                request, 'Unfortunately, something went wrong. Please try again.')
        auth_login(request, thisuser)
        return redirect('register')

    # karbar avalin bar ast be safhe register amade ast
    else:
        return render(request, 'signup.html', {})
#------------------------------------------------------------------------------#


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                messages.success(
                    request, 'Congratulations! You have successfully logged in. 😋')
                return redirect('login')  # go to home
            else:
                messages.error(
                    request, 'Your account is currently inactive!! 🥺')
                return redirect('register')
        else:
            messages.error(
                request, 'Username or password entered is incorrect!! 😑')
            return redirect('login')
    else:
        return render(request, 'login.html', {})
#------------------------------------------------------------------------------#


@login_required
def logout_view(request):
    django_logout(request)
    messages.success(request, 'You have successfully logged out. 🤐')
    return redirect('web:index')
#------------------------------------------------------------------------------#


def password_reset(request):
    # karbar email khod ra vared karde ast
    if 'resetPassword' in request.POST:
        if User.objects.filter(email=request.POST['email']).exists():
            userid = User.objects.get(email=request.POST['email']).id
            email = User.objects.get(id=userid).email
            username = User.objects.get(id=userid).username
            now = datetime.now()
            this_user = User.objects.get(email=email)
            token = password_reset_token(username, email, userid)
            passresetcode = Passwordresetcodes(
                user=this_user, code=token, time=now)
            passresetcode.save()
            messages.success(request, "<a href=\"{}?token={}&id={}\">\
			لینک رو به رو</a>".format(request.build_absolute_uri
                             ('/account/begin_password_reset/'), token, userid))
            return render(request, 'password_reset.html', {})
        else:
            messages.error(request, 'No user was found!? 😔')
            return redirect('password_reset')

    # karbar email ersal shode ra click karde ast
    elif 'token' in request.GET and 'id' in request.GET:
        code = request.GET['token']
        userid = request.GET['id']
        thisuser = get_object_or_404(User, id=userid)
        token = get_object_or_404(Passwordresetcodes, user=thisuser).code
        if code == token and thisuser.is_active == True:
            now = datetime.now()
            utc = pytz.UTC
            dt = now.replace(tzinfo=utc) - get_object_or_404(Passwordresetcodes,
                                                             user=thisuser).time.replace(tzinfo=utc)
            dt = dt.days
            if dt < 1:
                request.session['requested_user'] = userid
                return render(request, 'password_reset_confirm.html', {})
            else:
                Passwordresetcodes.objects.get(user=thisuser).delete()
                messages.error(
                    request, 'Your token has expired!!! 🤔 Request again (if you want 🤭)')
                return redirect('password_reset')
        elif code == token and thisuser.is_active == False:
            messages.warning(request, 'Sorry this account is disabled! 🤕')
        else:
            messages.error(
                request, 'Unfortunately, something went wrong. Please try again.')
            auth_login(request, thisuser)
            return redirect('password_reset')

    # karbar form password jadid ra por karde ast
    elif 'passconfirm' in request.POST:
        password = request.POST['password']
        password2 = request.POST['password2']
        userid = request.session.get('requested_user')
        thisuser = get_object_or_404(User, id=userid)
        if password == password2:
            password2 = None
            thisuser.set_password(request.POST['password'])
            thisuser.save()
            Passwordresetcodes.objects.get(user=thisuser).delete()
            messages.success(
                request, "Your password was changed successfully. 🥳")
            return redirect('login')
        else:
            messages.error(request, "The passwords entered are not match! 🤕")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # karbar avalin bar ast be safhe register amade ast
    else:
        return render(request, 'password_reset.html', {})
