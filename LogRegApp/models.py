from django.db import models
import bcrypt
import re
# Regexes
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.


class UserManager(models.Manager):
    def reg_val(self, postData):
        errors = {}
        # All validations for registering should happen here

        # First and Last name Validations
        if len(postData['f_name']) < 2:
            errors['reg_f_name'] = "Your first name must be at least 2 characters in length."
        elif not NAME_REGEX.match(postData['f_name']):
            errors['reg_f_name'] = "Your first name can only contain letters."
        if len(postData['l_name']) < 2:
            errors['reg_l_name'] = "Your last name must be at least 2 characters in length."
        elif not NAME_REGEX.match(postData['l_name']):
            errors['reg_l_name'] = "Your last name can only contain letters."

        # Email Validations

        if not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "You must enter a valid email address."

        existing = User.objects.filter(email=postData['email'])
        if len(existing) > 0:
            errors['reg_email'] = "A user with that email address already exists. Please log in or try another email address"

            # Password validations
        if len(postData['password']) < 8:
            errors['reg_pass'] = "Your password must be a minimum of 8 characters in length."
        elif postData['password'] != postData['pw_confirm']:
            errors['reg_pass'] = "Your passwords do not match."

        return errors

    def log_val(self, postData):
        errors = {}

        existing = User.objects.filter(email=postData['email'])
        if len(existing) == 0:
            errors['log'] = "Invalid username/password"
        else:
            if not bcrypt.checkpw(postData['password'].encode(), existing[0].password.encode()):
                errors['log'] = "Invalid username/password"

        return errors


class BookManager(models.Manager):
    def book_val(self, postData):
        errors = {}

        if len(postData['title']) < 1:
            errors['title'] = "You must include a book title."
        if len(postData['description']) < 5:
            errors['description'] = "You must write a description of at least 5 characters."

        return errors


class User(models.Model):
    f_name = models.CharField(max_length=35)
    l_name = models.CharField(max_length=35)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    posted_by = models.ForeignKey(
        User, related_name="books_posted", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="books_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
