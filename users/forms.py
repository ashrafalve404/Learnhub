from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import User


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar', 'bio', 'role', 'social_links', 'is_verified_instructor', 'phone', 'address']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar', 'bio', 'phone', 'address', 'social_links']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'bio':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
            elif field_name == 'social_links':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter as JSON: {"twitter": "url", "linkedin": "url"}'})
