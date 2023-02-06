from django.urls import path

from account import views as account_v

app_name = 'account'
urlpatterns = [
    path('login/', account_v.Login.as_view(), name='login'),
    path('logout/', account_v.Logout.as_view(), name='logout'),
    path('signup/', account_v.SignUp.as_view(), name='signup'),
    path('signup/done/', account_v.SignUpDone.as_view(), name='signupdone'),
]
