from django.db import models

# To Create A Custom User Model and admin panel
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy 
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class MyuserManager(
    BaseUserManager
):  # To Manage new users using this baseusermanaegr class
    """ A Custom User Manager to deal with Phone Number  as an unique Identifier """

    def _create_user(self, phone, username, password, **extra_fields):
        """Creates and Saves an user with given phone and password """

        if not phone:
            raise ValueError("phone Must Be Set")

        phone = self.normalize_email(phone)
        user = self.model(phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("SuperUser is_staff must be True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser is_superuser must be True")

        return self._create_user(phone, username, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, null=False, blank=False, unique=True)
    username = models.CharField(max_length=264,unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(
        gettext_lazy ("staff_status"),
        default=False,
        help_text="Determines Whether They Can Log in this Site or not",
    )
    is_active = models.BooleanField(
        gettext_lazy ("active"),
        default=True,
        help_text="Determines Whether their Account Status is Active or not",
    )
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]
    objects = MyuserManager()

    class Meta:
        verbose_name_plural = "User"
        db_table = "User"

    def __str__(self):
        return self.phone+"...."+self.username
