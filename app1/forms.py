from django import forms
class loginform(forms.Form):#creating a class named loginform that inherits from the base class forms.Form
    username = forms.CharField(#creating an instance of the class forms.CharField
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150,label='Username:', widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    firstname = forms.CharField(max_length=150,label='Username:', widget=forms.TextInput(attrs={'placeholder': 'Enter your First Name'}))
    lastname= forms.CharField(max_length=150,label='Username:', widget=forms.TextInput(attrs={'placeholder': 'Enter your Last Name'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))
    password = forms.CharField(label='Password:',widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    confirm_password = forms.CharField(label='Confirm Password:',widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))

class InputForm(forms.Form):
    description = forms.CharField(max_length=150,label='Enter Task:', widget=forms.TextInput(attrs={'placeholder': 'Enter your task here...'}))
    deadline = forms.DateField(label='Select a deadline', widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))

