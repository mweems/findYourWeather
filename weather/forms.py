from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	help = "Your password can't be too similar to your other personal information. Your password must contain at least 8 characters. Your password can't be a commonly used password. Your password can't be entirely numeric."
	current_city = forms.CharField(max_length=30, required=True, help_text='Your Current City')
	password1 = forms.CharField(widget=forms.PasswordInput(),label='Password', help_text=help)

	class Meta:
		model = User
		fields = ('username', 'current_city', 'password1', 'password2')

