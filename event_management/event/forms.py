# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'role', 'phone_number', 'address']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = [(choice[0], choice[1]) for choice in User.ROLE_CHOICES if choice[0] != 'admin']


from django import forms
from .models import Event

class CreateEventForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'id_start_time'})
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'id_end_time'})
    )
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'start_time', 'end_time']
