from django import forms
from .models import users as User

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    # field-level validation
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        if len(username) < 5:
            raise forms.ValidationError("Username must be at least 5 characters long.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data


from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username or len(username) < 5:
            raise forms.ValidationError("Username must be at least 5 characters long.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password or len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password.")
            cleaned_data["user"] = user  # Attach the authenticated user for view
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'fullname', 'phone', 'location']

    def clean_fullname(self):
        fullname = self.cleaned_data.get("fullname")
        if not fullname or len(fullname) < 5:
            raise forms.ValidationError("Full name must be at least 5 characters long.")
        return fullname

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        print(phone,len(phone))
        if not phone or len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone

    def clean_location(self):
        location = self.cleaned_data.get("location")
        if not location:
            raise forms.ValidationError("Location is required.")
        return location