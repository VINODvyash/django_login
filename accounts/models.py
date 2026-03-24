from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator

class Profile(models.Model):

    #Link Profile to User modell
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

#optional profile fields
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    age=models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    
    #Passwordreset system
    
    reset_otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.IntegerField(default=0)

#Timesstamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#Display username in admin panel
    def __str__(self):
        return self.user.username


#  creat model 

class Note(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="notes")
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default ='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
