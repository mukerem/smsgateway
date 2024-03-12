from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.timezone import now

from account.validators import phone_number_validator


role_list = (
    ("super admin", "super admin"),
    ("admin", "admin"),
    ("staff", "staff"),
    ("guest", "guest"),
)

class UserManager(BaseUserManager):
    def create_user(self, password,  email, first_name=' ', last_name=' '):
     
        if not email:
            raise ValueError('Users must have an email')
        
        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            register_date=timezone.now().date(),
        )
        user.set_password(password)
        user.email=self.normalize_email(email)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password
        """        
        user = self.create_user(
            first_name=' ',
            last_name=' ',
            email=email,
            password=password,
            role='super admin'
        )
        # user.email=self.normalize_email(email),
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone_number = models.CharField(
        max_length=14,
        validators=[phone_number_validator],
        unique=True,
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, choices=role_list)
    is_active = models.BooleanField(default=True)
    register_date = models.DateField(default = now)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
        
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.role == "super admin"
