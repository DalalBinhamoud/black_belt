from django.db import models
import re


emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
passwordRegex = re.compile(r'\d.*[A-Z]|[A-Z].*\d')
class validator(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # The email should have a valid format
        if not emailRegex.match(postData['email']):
            errors['email'] = "The email should be in valid format"

        #Name fields should be alphabetic
        if postData['username'].isalpha() ==  False:
            errors["username"] = "Name fields should be alphabetic"

        #Validate registration 
        temp = postData['username']
        username_exists = user_admin.objects.filter(username=temp)
        if len(username_exists) != 0:
            errors['username'] = " user name is already registered"

        # Password should be a minimum of 8 chars with at least one special char and 1 number
        if len(postData['password']) < 8:
            errors['password'] = "Password should be a minimum of 8 characters"
        elif not passwordRegex.match(postData['password']):
            errors['password'] = "Invalid Password, must have at least one Capital letter, at least one lower case letter and at least one number or special character"

        # Validate Confrim Password
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Passwords do not match"


        return errors
        
class user_admin(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = validator()

class files(models.Model):
    submitted_URL = models.TextField()
    result = models.TextField()
    respone = models.CharField(max_length=45)
    user_id = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class messages(models.Model):
#     message = models.TextField()
#     reciver_id = 
#     sender_id = 
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)