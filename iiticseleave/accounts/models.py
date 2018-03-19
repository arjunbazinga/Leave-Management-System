from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password ')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.user_type = 4
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,password)
        user.user_type = 0
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_types = ((0, 'Admin'),
                  (1, 'Supervisor'),
                  (2, 'Recommender'),
                  (3, 'Approver'),
                  (4, 'Standard')
                 )

    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(default='CSE',max_length=5)
    active = models.BooleanField(default=True)
    applicant = models.BooleanField(default=False)
    user_type = models.IntegerField(choices=user_types, default=4)
    c = ((0, 'Associate Professor'),
        (1, 'Assistant Professor'),
        (2, 'Professor'),
        (3, 'Other'))
    designation = models.IntegerField(choices=c, default=3)
    recommender = models.ForeignKey('accounts.User',
                                    on_delete=models.PROTECT,
                                    null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.


    def get_full_name(self):
        ans  = str(self.firstName)
        if self.lastName is not None:
            ans += " " + str(self.lastName)
        return ans

    def get_short_name(self):
        return self.firstName

    def __str__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        if perm in ['accounts.change_user', 'leave.change_application']:
            return True
        if self.is_admin:
            return True
        if self.is_applicant and perm in ['leave.add_application', 'leave.change_application', 'leave.delete_application']:
            return True
        return False

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_supervisor(self):
        "Is the user a supervisor?"
        return self.user_type == 1

    @property
    def is_recommender(self):
        "Is the user a recommender?"
        return self.user_type == 2

    @property
    def is_staff(self):
        "Is the user a staff?"
        return True

    @property
    def is_approver(self):
        "Is the user an approver?"
        return self.user_type == 3

    @property
    def is_standard(self):
        "Is the user standard?"
        return self.user_type == 4

    @property
    def is_admin(self):
        "Is the user an admin member?"
        return self.user_type == 0

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    @property
    def is_applicant(self):
        "Is the user an applicant?"
        return self.applicant
