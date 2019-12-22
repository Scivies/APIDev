from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
import uuid
import os
# Create your models here.
# Create abstract user model
# Auth user models

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    #split the filename, slice it with [-] then extract the extension with 1
    #1 is the extension position in the slice [-]
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)



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


class Recipe(models.Model):
    """Receipe object for all receipes"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
