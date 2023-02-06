from django.contrib.auth.forms import UserCreationForm

from account.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'name', 'address')
