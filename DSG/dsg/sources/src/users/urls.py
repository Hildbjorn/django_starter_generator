from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', UserUpdateView.as_view(), name='account'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('all_users/', AllUsersView.as_view(), name='all_users'),
    path('email_confirm_done/', email_confirm_done, name='email_confirm_done'),
    path('user_activate/<uidb64>/<token>/', user_activate, name='user_activate'),
]