from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password ')
        
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_supervisor_user(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.supervisor = True
        user.save(using=self._db)
        return user

    def create_recommendor_user(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.recommendor = True
        user.save(using=self._db)
        return user

    def create_approver_user(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.approver = True
        user.save(using=self._db)
        return user



    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    department = 'CSE'
    active = models.BooleanField(default=True)
    supervisor = models.BooleanField(default=False) 
    approver = models.BooleanField(default=False) 
    recommender = models.BooleanField(default=False)
    admin = models.BooleanField(default=False) # a superuser

    c = (
        (0, 'Associate Professor'),
        (1, 'Assistant Professor'),
        (2, 'Professor'),
        (3, 'Other'))
    designation = models.CharField(choices = c, max_length = 1, default = 0)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return str(self.firstName) + " " + str(self.lastName)

    def get_short_name(self):
        return self.firstName

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        print(app_label)
        # if self.is_admin and app_label in ['accounts']:
        return True
        return False

    @property
    def is_supervisor(self):
        "Is the user a supervisor?"
        return self.supervisor

    @property
    def is_recommender(self):
        "Is the user a recommender?"
        return self.recommender

    @property
    def is_staff(self):
        "Is the user a staff?"
        return True #everyone is a staff

    @property
    def is_approver(self):
        "Is the user an approver?"
        return self.approver

    @property
    def is_admin(self):
        "Is the user an admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active



