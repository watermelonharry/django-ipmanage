from models import CnTestSubscribeList
from django.forms import ModelForm


class CnTestSubscribeForm(ModelForm):
    class Meta:
        model = CnTestSubscribeList
        exclude = ['subscribeTime', 'testStatus', 'testLog']