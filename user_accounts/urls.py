from django.urls import path
from .views import SignUpView, activate_account

app_name = 'user_accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', activate_account, name='activate'),
]
