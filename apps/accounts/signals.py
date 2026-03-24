"""
Django Signals for Accounts Application
Handles automatic actions triggered by model changes.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance when a new User is created.
    
    Args:
        sender: Model class (User)
        instance: Instance of the model (User object)
        created: Boolean indicating if the object was created
        **kwargs: Additional arguments
    """
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the Profile instance when the User is saved.
    
    Args:
        sender: Model class (User)
        instance: Instance of the model (User object)
        **kwargs: Additional arguments
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    """
    Signal to clean up when a User is deleted.
    (Optional - can add custom cleanup logic here)
    
    Args:
        sender: Model class (User)
        instance: Instance of the model (User object)
        **kwargs: Additional arguments
    """
    try:
        if hasattr(instance, 'profile'):
            instance.profile.delete()
    except Profile.DoesNotExist:
        pass
