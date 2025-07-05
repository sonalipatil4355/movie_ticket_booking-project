from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from . models import User
from .forms import Identifyform
from django.utils import timezone
import datetime
from .utils import get_otp,enc_uname,dec_uname
from django.contrib.auth.forms import SetPasswordForm
from movies.models import Movie


# Create your views here.

# RegisterView function to handle user registration
def RegisterView(request):
    if request.method == 'POST':
        form = RegistrationForm(data = request.POST)
        if form.is_valid():
            form.save()
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            subject = 'Registration Successful'
            message = f'Hello {fname} {lname},\n\nThank you for registering with us. Your account has been created successfully.\n\nBest regards,\nMovie Ticket Booking Team'
            from_email = 'sp6700539@gmail.com'  
            recipient_list = [email]
            fail_silently = False
            send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently)
            
            messages.success(request, 'Registration successful! A confirmation email has been sent to your email address.')
            return redirect('login') 

    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
              
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # or use '/accounts/login/' if you prefer



@login_required
def HomeView(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})
 
def IdentifyUserView(request):
    if request.method == 'POST':
        form = Identifyform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                otp=get_otp()
                time = timezone.now() + datetime.timedelta(minutes=10)
                user.otp = otp
                user.otp_expired = time
                user.otp_verified=False
                email = user.email
                user.save()
                send_mail(
                    'OTP Verification',
                    f'Your OTP is {otp} enter otp to reset the password',
                    'sp6700539@gmail.com',
                    [email],
                    fail_silently=True,
                )
                messages.success(request,'user found otp has sent to registerd email')
                en_uname = enc_uname(user.username)
                url = f'/accounts/verifyotp/{en_uname}/'
                return redirect(url)
            messages.error(request,'user not found')
                
    context={
        'form' : Identifyform()
    }
    return render(request,'accounts/identify.html' , context)

def OTPView(request, en_uname):
    username = dec_uname(en_uname)
    if User.objects.filter(username=username).exists():
        if request.method == 'POST':
            otp1 = request.POST.get('otp1', '')
            otp2 = request.POST.get('otp2', '')
            otp3 = request.POST.get('otp3', '')
            otp4 = request.POST.get('otp4', '')
            otp_str = otp1 + otp2 + otp3 + otp4

            try:
                otp = int(otp_str)
            except ValueError:
                messages.error(request, 'Please enter a valid 4-digit OTP.')
                return redirect('identify')

            user = User.objects.get(username=username)
            if timezone.now() <= user.otp_expired:
                if not user.otp_verified:
                    if otp == user.otp:
                        user.otp_verified = True
                        user.save()
                        messages.success(request, 'OTP verified.')
                        url = f'/accounts/resetpassword/{en_uname}/'
                        return redirect(url)
                    else:
                        messages.error(request, 'Invalid OTP')
                        return redirect('identify')
                messages.error(request, 'OTP already verified')
                return redirect('identify')
            messages.error(request, 'OTP expired, please request a new one')
            return redirect('identify')
        return render(request, 'accounts/otp.html')
    messages.error(request, 'Invalid request')
    return redirect('login')

def ResetPasswordView(request,en_uname):
    try:
        username=dec_uname(en_uname)
    except:
        messages.error(request,'invalid request')
        return redirect('login')
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if request.method == 'POST':
            form = SetPasswordForm(user=user,data=request.POST)
            if form.is_valid():
                messages.success(request,'password reset successful')
                form.save()
                return redirect('login')
            else:
                messages.error(request,'invalid password or password and confirm password is not match')
        context ={
            'form' : SetPasswordForm(user=user)

        }
        return render(request, 'accounts/reset_password.html',context)
    messages.error(request,'invalid request')
    return redirect('login')  