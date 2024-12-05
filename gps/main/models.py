from django.db import models
from .validators import validate_reg_no, validate_kenyan_phone_number, validate_kenyan_id
from django.utils.timezone import now

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from .validators import validate_kenyan_id  # Assuming you have this custom validator


class Authorised_User(models.Model):
    national_id_no = models.DecimalField(max_digits=8, decimal_places=0, unique=True, validators=[validate_kenyan_id], help_text="Enter National Identification Number:")
    first_name = models.CharField(max_length=30, help_text="Enter First Name")
    last_name = models.CharField(max_length=30, help_text="Enter Last Name")
    email_address = models.EmailField(unique=True, max_length=50, help_text="Enter Email Address")
    username = models.EmailField(unique=True, max_length=50, help_text="Enter Username")
    phone_number = models.CharField(max_length=13, validators=[validate_kenyan_phone_number], help_text="Enter phone number in the format 0798073204 or +254798073404")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Owner(models.Model):
    national_id_no = models.DecimalField(max_digits=8, decimal_places=0, unique=True, validators=[validate_kenyan_id], help_text="Enter National Identification Number:")
    first_name = models.CharField(max_length=30, help_text="Enter First Name")
    last_name = models.CharField(max_length=30, help_text="Enter Last Name")
    email_address = models.EmailField(unique=True, max_length=50, help_text="Enter Email Address")
    username = models.EmailField(unique=True, max_length=50, help_text="Enter Username")
    phone_number = models.CharField(max_length=13, validators=[validate_kenyan_phone_number], help_text="Enter phone number in the format 0798073204 or +254798073404")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Laptop(models.Model):
    serial_number = models.CharField(max_length=20, primary_key=True, help_text="Enter Serial Number")
    mac_address = models.CharField(max_length=20, help_text="Enter Mac Address")
    model = models.CharField(max_length=50, help_text="Enter Model")
    unique_code = models.CharField(max_length=10, unique=True, help_text="Enter Unique Code")
    national_id_no = models.DecimalField(max_digits=8, decimal_places=0, unique=True, validators=[validate_kenyan_id], help_text="Enter National Identification Number:")

    def __str__(self):
        return f"Laptop: {self.model} - {self.unique_code}"

class Vehicle(models.Model):
    number_plate = models.CharField(max_length=20, primary_key=True, help_text="Enter Number Plate")
    model = models.CharField(max_length=50, help_text="Enter Model")
    unique_code = models.CharField(max_length=10, unique=True, help_text="Enter Unique Code")
    national_id_no = models.DecimalField(max_digits=8, decimal_places=0, unique=True, validators=[validate_kenyan_id], help_text="Enter National Identification Number:")

    def __str__(self):
        return f"Vehicle: {self.number_plate}"

class Item(models.Model):
    unique_code = models.CharField(max_length=10, unique=True, help_text="Enter Unique Code")
    pin = models.CharField(max_length=128)  # To store hashed PIN

    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)
        self.save()

    def __str__(self):
        return f"Item: {self.unique_code}"

class EntryLog(models.Model):
    unique_code = models.CharField(max_length=50, help_text="Enter Item Code")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.unique_code}"

class ExitLog(models.Model):
    unique_code = models.CharField(max_length=50, help_text="Enter Item Code")
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.timestamp} - {self.unique_code}"
    
class System_User(models.Model):
    username = models.EmailField(unique=True, max_length=50, help_text="Enter a valid Username")
    password_hash = models.CharField(max_length=128, help_text="Enter a valid password")

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def clean(self):
        # Custom validation for password field
        if len(self.password_hash) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

    def __str__(self):
        return self.username


class PasswordResetToken(models.Model):
    username = models.ForeignKey(System_User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.username}"

    def is_expired(self):
        expiration_time = self.created_at + timedelta(minutes=5)
        return timezone.now() > expiration_time