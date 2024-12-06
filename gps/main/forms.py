from django import forms
import re
from .models import (
    Owner, Laptop, Vehicle, Item, EntryLog, ExitLog, Authorised_User, System_User, PasswordResetToken
)

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    class Meta:
        model = System_User
        fields = ['username', 'password_hash']
        labels = {
            'username': 'Username',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username eg bornface@gmail.com'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance
    
class LoginForm(forms.Form):
    username = forms.EmailField(
        label="Username",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username:'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password:'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        return cleaned_data

class User_SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    class Meta:
        model = System_User
        fields = ['username', 'password_hash']
        labels = {
            'username': 'Username',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username eg bornface@gmail.com'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance
    
class User_LoginForm(forms.Form):
    username = forms.EmailField(
        label="Username",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username:'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password:'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        return cleaned_data



class LaptopOwnerForm(forms.Form):
    # Owner fields
    national_id_no = forms.DecimalField(
        max_digits=8, decimal_places=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner National Identification Number'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner Last Name'})
    )
    email_address = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner Email Address'})
    )
    phone_number = forms.CharField(
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner Phone Number'})
    )

    # Laptop fields
    serial_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Laptop Serial Number'})
    )
    mac_address = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Laptop MAC Address'})
    )
    model = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Laptop Model'})
    )


class VehicleOwnerForm(forms.Form):
    # Owner fields
    national_id_no = forms.DecimalField(
        max_digits=8, decimal_places=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner National Identification Number'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner Last Name'})
    )
    email_address = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner Email Address'})
    )
    phone_number = forms.CharField(
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner Phone Number'})
    )

    # Vehicle fields
    number_plate = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Vehicle Number Plate'})
    )
    model = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Vehicle Model'})
    )


class SetPinForm(forms.Form):
    unique_code = forms.CharField(max_length=10, help_text="Enter Item Unique Code")
    pin = forms.CharField(max_length=10, widget=forms.PasswordInput, help_text="Enter PIN (numeric)")

    def clean_pin(self):
        pin = self.cleaned_data['pin']
        if not pin.isdigit():
            raise forms.ValidationError("PIN must be numeric.")
        return pin

class ValidateEntryForm(forms.Form):
    unique_code = forms.CharField(max_length=10, help_text="Enter the item's unique code")

class ExitItemInitialForm(forms.Form):
    unique_code = forms.CharField(max_length=10, help_text="Enter the item's unique code")

class ExitItemPinForm(forms.Form):
    pin = forms.CharField(widget=forms.PasswordInput(), max_length=128, help_text="Enter the PIN")
    

class ModifyPinForm(forms.Form):
    unique_code = forms.CharField(
        max_length=10,
        help_text="Enter the unique code of the item.",
        widget=forms.TextInput(attrs={'placeholder': 'Unique Code', 'class': 'form-control'})
    )
    new_pin = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={'placeholder': 'New PIN', 'class': 'form-control'}),
        help_text="Enter your new PIN."
    )
    confirm_pin = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm PIN', 'class': 'form-control'}),
        help_text="Confirm your new PIN."
    )

    def clean(self):
        cleaned_data = super().clean()
        new_pin = cleaned_data.get('new_pin')
        confirm_pin = cleaned_data.get('confirm_pin')

        if new_pin != confirm_pin:
            raise forms.ValidationError("New PIN and Confirm PIN must match.")
        return cleaned_data

class ItemSearchForm(forms.Form):
    unique_code = forms.CharField(
        max_length=10,
        label="Enter Unique Code",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter unique code"}),
    )


class LogSearchForm(forms.Form):
    unique_code = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Unique Code'}),
        label="Item Unique Code"
    )

class PasswordResetForm(forms.Form):
    username = forms.EmailField(
        label='Username',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address(Username)'})
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not System_User.objects.filter(username=username).exists():
            raise forms.ValidationError("This Username is not associated with any account.")
        return username
    
 
class ResetForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    
    class Meta:
        model = System_User
        fields = ['password_hash']
        labels = {
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance    