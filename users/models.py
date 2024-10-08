from django.db import models
from PIL import Image
import uuid
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import cv2
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from ckeditor.fields import RichTextField

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **kwargs):
        if username is None:
            raise ValidationError("User Must Have A Password")
        if email is None:
            raise ValidationError("User Must Have An Email")
        if password is None:
            raise ValidationError("User Must Have A Password")
        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password, **kwargs):
        if username is None:
            raise ValidationError("SuperUser Must Have A Username")
        if email is None:
            raise ValidationError("SuperUser Must Have An Email")
        if password is None:
            raise ValidationError("SuperUser Must Have A Password")
        user = self.create_user(username=username, email=email, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
        


class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(blank=False, primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    username = models.CharField(unique=True, db_index=True, max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True, db_index=True)
    about = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='users_images')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser =  models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username
    

    @property
    def name(self):
        return self.first_name and self.last_name
    
    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            output = BytesIO()
            width, height = 100, 100
            img = img.resize((width, height))
            img_format = img.format  # Get the original image format
            if not img_format:  # If format is None, default to JPEG
                img_format = 'JPEG'
                img.save(output, format=img_format)
                output.seek(0)
                self.image = ContentFile(output.getvalue(), name=self.image.name)
        super().save(*args, **kwargs)
           

    objects = UserManager()








