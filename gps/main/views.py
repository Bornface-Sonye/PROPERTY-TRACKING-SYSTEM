from django import forms
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout  # Import the logout function

from django.views.generic import UpdateView, DeleteView, ListView, TemplateView, FormView
from django.shortcuts import get_object_or_404

from django.contrib import messages
import uuid
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .utils import generate_pdf
from .utils import generate_item_pdf
from django.http import HttpResponse

from .utils import *
from .models import (
    Owner, Laptop, Vehicle, Item, EntryLog, ExitLog, Authorised_User, System_User, PasswordResetToken
)

from .forms import (
   SignUpForm, LoginForm, LaptopOwnerForm, VehicleOwnerForm, SetPinForm, ValidateEntryForm, ExitItemInitialForm, 
   ExitItemPinForm, ModifyPinForm, ItemSearchForm, LogSearchForm, PasswordResetForm, ResetForm, User_SignUpForm,
   User_LoginForm
)

class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password_hash = form.cleaned_data['password_hash']
            
            if not Authorised_User.objects.filter(username=username).exists():
                # Add error message to the form
                form.add_error('username', "The username does not exist. Please register as an admin first.")
                return render(request, self.template_name, {'form': form})
            
            # Check if username already exists in System_User model
            if System_User.objects.filter(username=username).exists():
                form.add_error('username', "This username has already been used in the system!")
                return render(request, self.template_name, {'form': form})

            # Create the account if all checks pass
            new_account = form.save(commit=False)
            new_account.set_password(password_hash)
            new_account.save()
            return redirect('login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})
        
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
    
            user = System_User.objects.filter(username=username).first()
            if user and user.check_password(password):
                # Authentication successful
                request.session['username'] = user.username  # Store username in session
                return redirect(reverse('dashboard'))
            else:
                # Authentication failed
                error_message = 'Wrong Username or Password'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = 'Wrong Username or Password'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})
        
class User_SignUpView(View):
    template_name = 'user_signup.html'

    def get(self, request):
        form = User_SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = User_SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password_hash = form.cleaned_data['password_hash']
            
            if not Owner.objects.filter(username=username).exists():
                # Add error message to the form
                form.add_error('username', "The username does not exist. Please register an item first.")
                return render(request, self.template_name, {'form': form})
            
            # Check if username already exists in System_User model
            if System_User.objects.filter(username=username).exists():
                form.add_error('username', "This username has already been used in the system!")
                return render(request, self.template_name, {'form': form})

            # Create the account if all checks pass
            new_account = form.save(commit=False)
            new_account.set_password(password_hash)
            new_account.save()
            return redirect('user-login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})
        
        
class User_LoginView(View):
    template_name = 'user_login.html'

    def get(self, request):
        form = User_LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = User_LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
    
            user = System_User.objects.filter(username=username).first()
            if user and user.check_password(password):
                # Authentication successful
                request.session['username'] = user.username  # Store username in session
                return redirect(reverse('user-dashboard'))
            else:
                # Authentication failed
                error_message = 'Wrong Username or Password'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = 'Wrong Username or Password'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})
        
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)  
        return redirect('login')
    
class User_LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)  
        return redirect('user-login')

class DashboardView(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('login')

        # Fetch the system user
        try:
            system_user = System_User.objects.get(username=username)
        except System_User.DoesNotExist:
            return redirect('login')

        # Fetch the last name of the user from the Authorised_User table
        try:
            authorised_user = Authorised_User.objects.get(username=username)
            last_name = authorised_user.last_name
            first_name = authorised_user.first_name
        except Authorised_User.DoesNotExist:
            last_name = "Unknown"
            first_name = "User"

        # Fetch totals
        laptops_total = Laptop.objects.count()
        vehicles_total = Vehicle.objects.count()
        owners_total = Owner.objects.count()

        # Fetch first 10 laptops and vehicles
        laptops = Laptop.objects.all()[:10]
        vehicles = Vehicle.objects.all()[:10]

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'laptops_total': laptops_total,
            'vehicle_total': vehicles_total,
            'owners_total': owners_total,
            'laptops': laptops,
            'vehicles': vehicles,
        }

        return render(request, 'dashboard.html', context)

    
class User_DashboardView(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('user-login')

        # Fetch user details from System_User table
        try:
            user = System_User.objects.get(username=username)
        except System_User.DoesNotExist:
            return redirect('user-login')
        
        # Fetch the last name of the user from the Owner table
        try:
            owner = Owner.objects.get(username=username)
            last_name = owner.last_name
            first_name = owner.first_name
            national_id = owner.national_id_no  # Assuming this field exists in System_User
        except Owner.DoesNotExist:
            last_name = "Unknown"
            first_name = "User"
      
        national_id_no = national_id

        # Laptop and Vehicle counts and details
        laptops = Laptop.objects.filter(national_id_no=national_id_no)
        vehicles = Vehicle.objects.filter(national_id_no=national_id_no)

        laptops_total = laptops.count()
        vehicles_total = vehicles.count()

        laptop_serial_numbers = laptops.values_list('serial_number', flat=True)
        vehicle_number_plates = vehicles.values_list('number_plate', flat=True)

        # Administrator Details
        admin_user = Authorised_User.objects.first()  # Assuming there's at least one admin
        admin_last_name = admin_user.last_name if admin_user else "Not Available"

        # Entries and Exits
        vehicle_codes = vehicles.values_list('unique_code', flat=True)
        laptop_codes = laptops.values_list('unique_code', flat=True)

        entries = EntryLog.objects.filter(unique_code__in=list(vehicle_codes) + list(laptop_codes)).count()
        exits = ExitLog.objects.filter(unique_code__in=list(vehicle_codes) + list(laptop_codes)).count()

        # Prepare context
        context = {
            'admin_name': admin_last_name,
            'last_name': last_name,
            'laptops_total': laptops_total,
            'vehicle_total': vehicles_total,
            'entries': entries,
            'exits': exits,
            'laptops': laptops,
            'vehicles': vehicles,
        }

        return render(request, 'user_dashboard.html', context)


class Register_LaptopView(View):
    template_name = 'register_laptop.html'

    def get(self, request):
        form = LaptopOwnerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LaptopOwnerForm(request.POST)
        if form.is_valid():
            # Extract owner data
            national_id_no = form.cleaned_data['national_id_no']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email_address = form.cleaned_data['email_address']
            phone_number = form.cleaned_data['phone_number']

            # Extract laptop data
            serial_number = form.cleaned_data['serial_number']
            mac_address = form.cleaned_data['mac_address']
            model = form.cleaned_data['model']

            # Check for duplicate laptop
            if Laptop.objects.filter(serial_number=serial_number).exists():
                form.add_error(None, "A laptop with this serial number already exists!")
                return render(request, self.template_name, {'form': form})

            # Create or get the owner
            owner, created = Owner.objects.get_or_create(
                national_id_no=national_id_no,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email_address': email_address,
                    'username': email_address,
                    'phone_number': phone_number,
                }
            )

            if not created:
                # Check if the provided details match the existing owner
                if (owner.first_name != first_name or owner.last_name != last_name or 
                    owner.email_address != email_address or owner.phone_number != phone_number):
                    form.add_error(None, "Owner details do not match with existing records!")
                    return render(request, self.template_name, {'form': form})

            # Create the laptop
            unique_code = str(uuid.uuid4())[:8]  # Generate a unique 8-character code
            laptop = Laptop(
                serial_number=serial_number,
                mac_address=mac_address,
                model=model,
                unique_code=unique_code,
                national_id_no=national_id_no,
            )
            laptop.save()

            messages.success(request, f"Laptop registered successfully! Unique Code: {unique_code}")
            return render(request, self.template_name, {'form': LaptopOwnerForm()})

        # Form is invalid
        messages.error(request, "Failed to register laptop. Please correct the errors and try again.")
        return render(request, self.template_name, {'form': form})

        
class Register_VehicleView(View):
    template_name = 'register_vehicle.html'

    def get(self, request):
        form = LaptopOwnerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = VehicleOwnerForm(request.POST)
        if form.is_valid():
            # Extract owner data
            national_id_no = form.cleaned_data['national_id_no']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email_address = form.cleaned_data['email_address']
            phone_number = form.cleaned_data['phone_number']

            # Extract laptop data
            number_plate = form.cleaned_data['number_plate']
            model = form.cleaned_data['model']

            # Check for duplicate vehicle
            if Vehicle.objects.filter(number_plate=number_plate).exists():
                form.add_error(None, "A vehicle with this number plate already exists!")
                return render(request, self.template_name, {'form': form})

            # Create or get the owner
            owner, created = Owner.objects.get_or_create(
                national_id_no=national_id_no,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email_address': email_address,
                    'username': email_address,
                    'phone_number': phone_number,
                }
            )

            if not created:
                # Check if the provided details match the existing owner
                if (owner.first_name != first_name or owner.last_name != last_name or 
                    owner.email_address != email_address or owner.phone_number != phone_number):
                    form.add_error(None, "Owner details do not match with existing records!")
                    return render(request, self.template_name, {'form': form})

            # Create the vehicle
            vehicle = Vehicle(
                number_plate=number_plate,
                model=model,
                unique_code=number_plate,
                national_id_no=national_id_no,
            )
            vehicle.save()

            messages.success(request, f"Vehicle registered successfully!")
            return render(request, self.template_name, {'form': VehicleOwnerForm()})

        # Form is invalid
        messages.error(request, "Failed to register vehicle. Please correct the errors and try again.")
        return render(request, self.template_name, {'form': form})
    
class SetItemPinView(View):
    template_name = 'set_item_pin.html'

    def get(self, request):
        """Handles GET requests to display the form."""
        form = SetPinForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Handles POST requests to process the form."""
        form = SetPinForm(request.POST)
        if form.is_valid():
            unique_code = form.cleaned_data['unique_code']
            pin = form.cleaned_data['pin']

            # Check if unique code exists in Laptop or Vehicle
            if not (Laptop.objects.filter(unique_code=unique_code).exists() or 
                    Vehicle.objects.filter(unique_code=unique_code).exists()):
                messages.error(request, "Unique code does not exist in Laptop or Vehicle records.")
            else:
                # Create or update Item record
                item, created = Item.objects.get_or_create(unique_code=unique_code)
                item.set_pin(pin)
                messages.success(request, "PIN set successfully.")
                return redirect('set-item-pin')  # Redirect to the same page or another appropriate page

        return render(request, self.template_name, {'form': form})

class ValidateItemEntryView(View):
    template_name = 'validate_item_entry.html'

    def get(self, request):
        """Handles GET requests to display the form."""
        form = ValidateEntryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Handles POST requests to process the form."""
        form = ValidateEntryForm(request.POST)
        if form.is_valid():
            unique_code = form.cleaned_data['unique_code']

            # Check if the unique code exists in the Item table
            item = Item.objects.filter(unique_code=unique_code).first()
            if not item:
                messages.error(request, "The entered unique code does not exist.")
            else:
                # Log the entry
                EntryLog.objects.create(
                    unique_code=unique_code,
                )
                messages.success(request, "Entry logged successfully.")
                return redirect('validate-item-entry')  # Redirect to the same page or another

        return render(request, self.template_name, {'form': form})

class AuthenticateItemExitView(View):
    template_name = 'authenticate_item_exit.html'

    def get(self, request):
        """Handles GET requests to display the initial form."""
        form = ExitItemInitialForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Handles POST requests for item exit authentication."""
        if 'unique_code' in request.POST:  # Step 1: Verify unique code
            form = ExitItemInitialForm(request.POST)
            if form.is_valid():
                unique_code = form.cleaned_data['unique_code']
                item = Item.objects.filter(unique_code=unique_code).first()

                if not item:
                    messages.error(request, "The entered unique code does not exist.")
                else:
                    # Load the PIN form if unique code exists
                    pin_form = ExitItemPinForm()
                    return render(request, self.template_name, {'pin_form': pin_form, 'unique_code': unique_code})

        elif 'pin' in request.POST:  # Step 2: Verify PIN
            pin_form = ExitItemPinForm(request.POST)
            unique_code = request.POST.get('unique_code')
            item = Item.objects.filter(unique_code=unique_code).first()

            if item and pin_form.is_valid():
                pin = pin_form.cleaned_data['pin']
                if check_password(pin, item.pin):
                    # Log the exit
                    ExitLog.objects.create(
                        unique_code=unique_code,
                    )
                    messages.success(request, "Exit logged successfully.")
                    return redirect('authenticate-item-exit')
                else:
                    messages.error(request, "Incorrect PIN. Please try again.")
            else:
                messages.error(request, "Invalid operation. Please try again.")

        # Display the initial form if no valid data
        form = ExitItemInitialForm()
        return render(request, self.template_name, {'form': form})
    
@method_decorator(csrf_protect, name='dispatch')
class ModifyPinView(View):
    template_name = 'modify_pin.html'
    form_class = ModifyPinForm

    def get(self, request, *args, **kwargs):
        # Retrieve username from session
        username = request.session.get('username')
        if not username:
            return redirect('user-login')  # Redirect to login if username is missing
        
        # Render the form for GET requests
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Retrieve username from session
        username = request.session.get('username')
        if not username:
            return redirect('user-login')  # Redirect to login if username is missing

        form = self.form_class(request.POST)
        if form.is_valid():
            unique_code = form.cleaned_data['unique_code']
            new_pin = form.cleaned_data['new_pin']

            # Retrieve the user's national_id_no from the Owner table
            owner = get_object_or_404(Owner, username=username)
            user_national_id_no = owner.national_id_no

            # Perform union of Laptop and Vehicle to find items with the user's national_id_no
            laptops = Laptop.objects.filter(national_id_no=user_national_id_no)
            vehicles = Vehicle.objects.filter(national_id_no=user_national_id_no)

            # Combine laptops and vehicles unique codes
            valid_codes = set(laptops.values_list('unique_code', flat=True)) | set(vehicles.values_list('unique_code', flat=True))

            if unique_code not in valid_codes:
                messages.error(request, "The unique code does not match your items.")
            else:
                # Update the PIN of the item
                item = get_object_or_404(Item, unique_code=unique_code)
                item.set_pin(new_pin)
                messages.success(request, f"PIN for item {unique_code} has been successfully modified.")
        
        # Render the form with success or error messages
        return render(request, self.template_name, {'form': form})


class ItemReportView(View):
    template_name = "item_report.html"

    def format_key(self, key):
        """Helper function to format the dictionary keys."""
        return key.replace('_', ' ').capitalize()

    def get(self, request):
        form = ItemSearchForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ItemSearchForm(request.POST)
        if form.is_valid():
            unique_code = form.cleaned_data["unique_code"]
            
            # Check in Laptop model
            laptop = Laptop.objects.filter(unique_code=unique_code).first()
            if laptop:
                owner = Owner.objects.filter(national_id_no=laptop.national_id_no).first()
                details = {
                    "unique_code": laptop.unique_code,
                    "serial_number": laptop.serial_number,
                    "mac_address": laptop.mac_address,
                    "model": laptop.model,
                    "owner_national_id": owner.national_id_no,
                    "owner_name": f"{owner.first_name} {owner.last_name}",
                    "owner_phone": owner.phone_number,
                    "owner_email": owner.email_address,
                }
                
                # Format the keys in the details dictionary
                formatted_details = {self.format_key(key): value for key, value in details.items()}
                
                context = {
                    "form": form,
                    "item": "Laptop",
                    "details": formatted_details,
                }
                return render(request, self.template_name, context)
            
            # Check in Vehicle model
            vehicle = Vehicle.objects.filter(unique_code=unique_code).first()
            if vehicle:
                owner = Owner.objects.filter(national_id_no=vehicle.national_id_no).first()
                details = {
                    "unique_code": vehicle.unique_code,
                    "number_plate": vehicle.number_plate,
                    "model": vehicle.model,
                    "owner_national_id": owner.national_id_no,
                    "owner_name": f"{owner.first_name} {owner.last_name}",
                    "owner_phone": owner.phone_number,
                    "owner_email": owner.email_address,
                }
                
                # Format the keys in the details dictionary
                formatted_details = {self.format_key(key): value for key, value in details.items()}
                
                context = {
                    "form": form,
                    "item": "Vehicle",
                    "details": formatted_details,
                }
                return render(request, self.template_name, context)
            
            # If no match found
            messages.error(request, "No item found with the provided unique code.")
        
        return render(request, self.template_name, {"form": form})

class LogSearchView(View):
    template_name = 'log_search.html'

    def get(self, request):
        form = LogSearchForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LogSearchForm(request.POST)
        context = {'form': form}

        if form.is_valid():
            unique_code = form.cleaned_data['unique_code']
            
            # Query Entry and Exit Logs
            entry_logs = EntryLog.objects.filter(unique_code=unique_code).order_by('timestamp')
            exit_logs = ExitLog.objects.filter(unique_code=unique_code).order_by('timestamp')
            
            context.update({
                'unique_code': unique_code,
                'entry_logs': entry_logs,
                'exit_logs': exit_logs,
            })

            # Generate PDF on request
            if 'download_pdf' in request.POST:
                return generate_pdf(unique_code, entry_logs, exit_logs)

        return render(request, self.template_name, context)
    
class ResetPasswordView(View):
    template_name = 'reset_password.html'
    form_class = PasswordResetForm
    success_redirect_url = 'home'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = System_User.objects.filter(username=username).first()
            if user:
                try:
                    # Generate a unique token
                    token = get_random_string(length=32)
                    # Save the token to the database
                    PasswordResetToken.objects.create(username=user, token=token)
                    # Generate the correct reset link
                    
                    email = System_User.objects.filter(username=user).first()
                    reset_link = request.build_absolute_uri(f'/Linker/reset-password/{token}/')
                    # Send password reset email
                    send_mail(
                        'Reset Your Password',
                        f'Click the link to reset your password: {reset_link}',
                        settings.EMAIL_HOST_USER,
                        [email.email_address],
                        fail_silently=False,
                    )
                    return redirect(self.success_redirect_url)
                except Exception as e:
                    error_message = f"An error occurred: {str(e)} or Email Address does not exist in our records"
                    return render(request, self.template_name, {'form': form, 'error_message': error_message})
            else:
                error_message = "Email Address does not exist in our records."
                return render(request, self.template_name, {'form': form, 'error_message': error_message})

        return render(request, self.template_name, {'form': form})


class ResetPasswordConfirmView(View):
    template_name = 'reset_password_confirm.html'
    form_class = ResetForm

    def get(self, request, token):
        # Check if the token exists in the database
        password_reset_token = PasswordResetToken.objects.filter(token=token).first()
        if not password_reset_token or password_reset_token.is_expired():
            error_message = "Token is invalid or expired. Try resetting your password again."
            return render(request, self.template_name, {'error_message': error_message})

        # Initialize the form for GET requests
        form = self.form_class()

        # Render the form in the template
        return render(request, self.template_name, {'form': form, 'token': token})

    def post(self, request, token):
        # Check if the token exists in the database
        password_reset_token = PasswordResetToken.objects.filter(token=token).first()
        if not password_reset_token or password_reset_token.is_expired():
            error_message = "Token is invalid or expired. Try resetting your password again."
            return render(request, self.template_name, {'error_message': error_message})

        # Process the form submission
        form = self.form_class(request.POST)
        if form.is_valid():
            password_hash = form.cleaned_data['password_hash']
            reset = get_object_or_404(PasswordResetToken, token=password_reset_token)
            user = get_object_or_404(System_User, username=reset.username)
            
            # Delete the user (if this is the desired behavior)
            user.delete()
            
            # Create the new account
            account = form.save(commit=False)
            account.username = reset.username
            account.set_password(password_hash)
            account.save()

            # Delete the token
            password_reset_token.delete()

            # Redirect to the login page
            return redirect('login')

        # Render the form again with errors if invalid
        return render(request, self.template_name, {'form': form, 'token': token, 'error_message': "Invalid form submission. Please check your input."})


