from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',HomeView,name="Home"),
    path('login/',UsersLoginView.as_view(),name="UserLogin"),
    path('contact-us/',ContactUsView.as_view(),name="ContactUs"),
    path('about-us/',aboutUs, name="AboutUs"),
    path('privacy-policy/',privacyPolicy, name="PrivacyPolicy"),

    # Sign Up process urls
    path('signup-step-1/',SignUpView1.as_view(),name="SignUpStep1"),
    path('signup-step-2/<str:key>',SignUpView2.as_view(),name="SignUpStep2"),

    # User account related urls
    path('logout/',logoutView,name="LogoutView"),

    # Password handling related urls (we have put these url in this section because both admin and user will use these views)
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="password-reset-templates/reset_password.html"),
    name="reset_password"),

    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name="password-reset-templates/reset_password_sent.html"),
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="password-reset-templates/reset_password_form.html"),
    name="password_reset_confirm"),

    path('password_reset_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-templates/reset_password_completed.html"),
    name="password_reset_complete"),

    path('password_change/',
    auth_views.PasswordChangeView.as_view(template_name="password-reset-templates/password_change.html"),
    name="password_change"),

    path('password_change_done/',
    auth_views.PasswordChangeDoneView.as_view(template_name="password-reset-templates/password_changed.html"),
    name="password_change_done"),

]
