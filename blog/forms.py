from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.models import User

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label="Text", widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model =Post
        fields = (
            'title',
            'body',
            'status',
        )


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Enter Password Here...', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password...', 'class': 'form-control'}))
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="last Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="EmailAddress", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password Mismatch")
        return confirm_password


class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

class ProfileEditForm(forms.ModelForm):
    dob = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
   

    class Meta:
        model = Profile
        exclude = ('user',)
        fields = (
                'dob',  
                'photo',              
            )


class PostEditForm(forms.ModelForm):
    class Meta:
        model =Post
        fields = (
            'title',
            'body',
            'status',
        )


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text goes here!!!', 'rows':'4', 'col':'50'}))
    class Meta:
        model = Comment
        fields = ('content',)