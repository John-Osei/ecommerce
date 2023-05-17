from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path("sign-up/", views.register_view, name="sign-up"),
    path("sign-in/", views.login_view, name="sign-in"),
    path("sign-out/", views.logout_view, name="sign-out"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('social/signup', views.signup_redirect, name='signup_redirect'),

    # path("newsletter", views.newsletter, name ="newsletter"),


    path("password-reset/", views.password_reset_request, name="reset-password"),
    path("password-change/", views.password_change, name="password-change"),
    path("reset/<uidb64>/<token>", views.passwordResetConfirm, name="password-reset-confirm"),

    path("profile/update/", views.profile_update, name="profile-update"),
]