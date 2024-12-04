from django.contrib import admin
from .models import (
    Owner, Laptop, Vehicle, Item, EntryLog, ExitLog, Authorised_User, System_User
)

models_to_register = [
Owner, Laptop, Vehicle, Item, EntryLog, ExitLog, Authorised_User, System_User
    
]

i = 0
while True:
    admin.site.register(models_to_register[i])
    i += 1
    if i >= len(models_to_register):
        break
