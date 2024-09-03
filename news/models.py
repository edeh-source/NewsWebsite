from django.db import models
from users.models import User

from django.utils.text import slugify
from PIL import Image
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager
import cv2
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from io import BytesIO
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from django.conf import settings




class Category(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=256)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

        


    def get_absolute_url(self):
        return reverse('category_details', args=[self.slug])    
    
    class Meta:
        ordering = ['-created', '-id']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

        indexes = [
            models.Index(fields=['-created', '-id']),
        ]
    

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors',)
    email = models.EmailField(blank=True)
    about = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username    

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique_for_date='publish', blank=True)
    active = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='posts')
    publish = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='posts_images/')
    text = RichTextField()
    views = views = models.PositiveIntegerField(default=0)
    tags = TaggableManager()
    videos = EmbedVideoField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ['-created']

        indexes = [
            models.Index(fields=['-created', '-id']),
        ]


    def get_absolute_url(self):
        return reverse('post_details', args=[self.id, self.slug, self.publish.year, self.publish.month, self.publish.day])
    
    def get_publisher_url(self):
        return reverse('publisher_details', args=[self.id, self.slug, self.publish.year, self.publish.month, self.publish.day])


    def __str__(self):
        return self.name
    
    
    


    

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            output = BytesIO()
            width, height = 900, 630
            img = img.resize((width, height))
            img_format = img.format  # Get the original image format
            if not img_format:  # If format is None, default to JPEG
                img_format = 'JPEG'
                img.save(output, format=img_format)
                output.seek(0)
                self.image = ContentFile(output.getvalue(), name=self.image.name)
        super().save(*args, **kwargs)
        

    

class Comment(models.Model):
    post = models.name = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(to='users.User', related_name='comments', on_delete=models.CASCADE, default='ba94a1b9-8dce-4e5c-a0df-be383b13a070')
    name = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post} on {self.body}'



class Reply(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Reply by {self.user} on {self.comment} '
        

class Message(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    messages = models.TextField()

    def __str__(self):
        return f'Message by {self.name} and {self.email}'
        
                
    