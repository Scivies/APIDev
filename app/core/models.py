from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
# Create your models here.
# Create abstract user model
# Auth user models

class UserManager(BaseUserManager):
# Create and save new user
# ***extra_fields will automatically add any additional fields
# Use the normalize email function so all emails are lowercase
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have a valid email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user


# Create and save a new superuser
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Create the user models
# Custom user model that supports using email instead of username
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'email'

class Tag(models.Model):
    """Tag to be used for receipe and other apps"""
    name = models.CharField(max_length=255)
    #assign a foriegn key to the user models and what happes to the tags,
    #when the user is deleted.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,

    )

    #Add the tag strings to the model
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Ingredient to be used in a receipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    #Add the function to transform ingredient(s) to a string
    def __str__(self):
        return self.name
