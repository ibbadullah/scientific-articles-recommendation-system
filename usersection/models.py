from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager)


# Overriding base user manager
class MyAccountManager(BaseUserManager):
    # We can pass extra parameters from the create_user function
    def create_user(self,email,username,password,first_name,last_name):
        if not email:
            raise ValueError("The user must have an email.")
        if not username:
            raise ValueError("The user must have a username.")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )

        # Setting password and saving in database
        user.set_password(password)
        user.save(using=self.db)
        return user


    # Creating superuser
    def create_superuser(self,email,username,password,first_name,last_name):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password
        )

        # Now changing the default values
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        # Saving admin
        user.save(using=self.db)
        return user


# Overriding base user model (In order to change username as a login field to email)
class SignUpModel(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',unique=True)
    username = models.CharField(max_length=100,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.TextField(max_length=255,blank=True,null=True,default=False)
    last_name = models.TextField(max_length=255,blank=True,null=True,default=False)
    # USERNAME_FIELD = "email" is a bit confusing. But it is built-in from the Django side.
    # Actually we are changing username field to email, which means user will login on email instead of username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    # function for returning email
    def __str__(self):
        return self.email

    # function for returning the is_admin
    def has_perm(self,perm,obj=None):
        return self.is_admin

    # giving module permission
    def has_module_perms(self,app_label):
        return True



# Model for storing user interested articles
class Doc2VecModel(models.Model):
    User = models.ForeignKey(SignUpModel,verbose_name="user",on_delete=models.CASCADE)
    Article = models.ForeignKey("adminsection.ArticlesModel",verbose_name="article",on_delete=models.CASCADE)
    read_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "doc2vecmodel"
