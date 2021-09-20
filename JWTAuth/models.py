from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    This model is used for create custom user. Username should be email and unique.
    """
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    company = models.CharField(db_index=True, max_length=255)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(db_index=True, max_length=255, blank=True)
    is_manager = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    username = models.EmailField(max_length=150, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.firstname, self.lastname
