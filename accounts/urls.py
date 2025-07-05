from django.urls import path
from .views import HomeView, RegisterView, LoginView, logout_view,IdentifyUserView,OTPView,ResetPasswordView

urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('login/', LoginView, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', HomeView, name='home'), 
    path('identify/', IdentifyUserView, name='identify'),
    path('verifyotp/<en_uname>/', OTPView, name='otp'),
    path('resetpassword/<en_uname>/',ResetPasswordView,name='ResetPassword')
    
]
