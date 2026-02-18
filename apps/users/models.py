from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El campo Email debe estar definido")
        if not password:
            raise ValueError("El superusuario debe tener contraseña.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El campo Email debe estar definido")
        if not password:
            raise ValueError("El usuario debe tener contraseña")
    
        # when they use create_superuser(email="admin@test.com",password="1234")
        # and it doesnt have the is_staff parameter
        # if some pass is_staff=False it doesnt enter here and go to the validations
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Create your models here.
class CustomUser(AbstractUser):
    # we can delete username if not needed
    username = None  
    email = models.EmailField(unique=True)

    # avatar = models.ImageField(
    #     upload_to="avatars/",
    #     null=True,
    #     blank=True,
    #     default="avatars/default.png"
    # )

    USERNAME_FIELD = "email"   # login is with email
    REQUIRED_FIELDS = []       #

    objects = CustomUserManager()  # use manager

    def __str__(self):
        return self.email