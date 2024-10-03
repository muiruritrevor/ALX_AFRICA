from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# custom manager class that extends BaseUserManager
class UserManager(BaseUserManager):
# creating a new user
    def create_user(self, first_name, last_name, email, username, password=None):
        if not email:
            raise ValueError('Enter email address')
        
        if not username:
            raise ValueError('Enter username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

# creating a new superuser
    def create_superuser(self, first_name,last_name, email, username, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
            password=password,
            
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# A custom user model that extends AbstractUser class   
class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def checked_out_books(self):
        """Get a list of books currently checked out by the user."""
        return Book.objects.filter(transactions__user=self, transactions__transaction_type='CO', transactions__return_date__isnull=True)

    def reserved_books(self):
        """Get a list of books currently reserved by the user."""
        return Book.objects.filter(transactions__user=self, transactions__transaction_type='RS', transactions__return_date__isnull=True)

    def __str__(self):
        return self.email

class Profile(models.Model):
    pic = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(max_length=500, blank=True)
