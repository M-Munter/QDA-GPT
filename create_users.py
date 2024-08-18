# create_users.py
# This script creates user accounts in a Django application using credentials stored in environment variables.

import os
import django
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the Django environment by specifying the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User

# List of users to create, reading from environment variables
users = [
    {
        'username': os.getenv('USER1_USERNAME'),
        'password': os.getenv('USER1_PASSWORD')
    },
    {
        'username': os.getenv('USER2_USERNAME'),
        'password': os.getenv('USER2_PASSWORD')
    },
    {
        'username': os.getenv('USER3_USERNAME'),
        'password': os.getenv('USER3_PASSWORD')
    }
]

# Create users
for user_data in users:
    if user_data['username'] and user_data['password']:
        # Check if the user already exists, if not, create a new user
        user, created = User.objects.get_or_create(username=user_data['username'])
        if created:
            # Set the user's password and save the user object
            user.set_password(user_data['password'])
            user.save()
            print(f"User {user_data['username']} created.")
        else:
            print(f"User {user_data['username']} already exists.")
    else:
        print(f"Invalid data for user {user_data}")
