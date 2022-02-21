# This file allows custom users to be created instead of using django's in built user class
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

class AccountManager(BaseUserManager):
    
    # Method to create a customer
    def create_customer(self,f_name, l_name, email, password):
        # encrypt the users password
        try:
            password = make_password(password)
        except:
            print("There was an issue encrypting the password")
            return
        # make sure there is an email and password present
        if not email:
            raise ValueError("Email address must be provided")
        try:
            user = self.model(
                f_name =f_name, 
                l_name = l_name,
                email = self.normalize_email(email),    #   make the email lowercase
                password = password
            )
            user.save()
            return user
        except:
            print("There was an issue creating the least privileged account")
            
    # Method to create a staff member
    def create_staffmember(self, f_name, l_name, email, password):
        try:
            # use the customer creation method as a base
            try:
                user = self.create_customer(f_name, l_name, email, password)
            except:
                print("There was an issue with creating the base user for a staff member")
                return
            # add additional details to the base
            user.is_admin = True
            user.is_staff = True
            user.save
            return user
        except:
            print("There was an issue creating this staff member")
       
    # Method to create a superuser 
    def create_superuser(self,f_name, l_name, email, password):
        try:
            # use the staff member creation method as a base
            try:
                user = self.create_staffmember(f_name, l_name, email, password)
            except:
                print("There was an issue with creating the base user for a superuser")
                return
            user.is_superuser = True
            user.save()
            return user
        except:
            print("There was an issue creating this superuser")
            

class CustomUser(AbstractBaseUser, PermissionsMixin):
    f_name = models.CharField(verbose_name = 'First Name', max_length = 40, default = '')
    l_name = models.CharField(verbose_name = 'Last Name', max_length = 40, default = '')
    email = models.EmailField(verbose_name = 'email', max_length = 40, unique = True)
    member_since = models.DateTimeField(verbose_name = 'member since', auto_now_add = True) # this variable value is automatically set wit hthe current date/time when account is created
    last_login = models.DateTimeField(verbose_name = 'last login', auto_now = True) # this variable will be overwritten with a new value everytime the user logs in
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    objects = AccountManager()
    
    USERNAME_FIELD = 'email'    # this allows user to sign in with their email address rather than a user name
    REQUIRED_FIELDS = ['f_name', 'l_name']
    
    def __str__(self):
        return self.email
        
    def is_admin_user(self):
        return self.is_admin
        
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
