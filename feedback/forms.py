from django.forms import ModelForm

from feedback.models import FeedBackModel


class FeedBackForm(ModelForm):
    class Meta:
        model = FeedBackModel
        exclude = ['create_time', 'edit_time', 'id']