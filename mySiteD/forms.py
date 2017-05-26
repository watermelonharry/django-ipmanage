from django.contrib.auth.models import User
from django.forms import ModelForm


class UserFrom(ModelForm):
    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'date_joined','last_login', 'is_superuser', 'groups']