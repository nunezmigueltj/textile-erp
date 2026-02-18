from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password")
            if not user.is_active:
                raise forms.ValidationError("This account is not active.")
            cleaned_data["user"] = user
        return cleaned_data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
                            "class": "form-control"
                        }), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
                            "class": "form-control"
                        }), label="Confirm Password")

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "is_superuser"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "is_superuser": forms.CheckboxInput(attrs={"class": "form-check-input"},),
        }


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match.")
        return password2

    def save(self, should_commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if should_commit:
            user.save()
        return user

