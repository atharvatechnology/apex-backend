from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from accounts.models import Profile
from common.decorators import disable_for_loaddata

User = get_user_model()


@disable_for_loaddata
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(
        user=instance,
        defaults={
            "user": instance,
        },
    )


@disable_for_loaddata
@receiver(post_save, sender=User)
def delete_redis_cache_on_inactive_user(sender, instance, created, **kwargs):
    """Delete the Redis cache for a user's auth token when the user is marked inactive.

    This function is triggered by the post-save signal for the User model.
    If the user is marked as inactive, it deletes the Redis cache entry
    for the user's authentication token.

    Args:
        sender: The sender of the signal (User).
        instance: The instance of the User model that was saved.
        created: A boolean indicating whether the instance was created.
        **kwargs: Additional keyword arguments passed to the signal handler.

    Returns
        None

    """
    if not instance.is_active:
        user_id = instance.id
        cache.delete(f"{user_id}-token")


@receiver(post_delete, sender=User)
def delete_redis_cache_on_delete_user(sender, instance, **kwargs):
    """Delete the Redis cache for a user's auth token when the user is deleted.

    This function is triggered by the post-delete signal for the User model.
    It deletes the Redis cache entry for the user's authentication token.

    Args:
        sender: The sender of the signal (User).
        instance: The instance of the User model that was deleted.
        **kwargs: Additional keyword arguments passed to the signal handler.

    Returns
        None

    """
    user_id = instance.id
    cache.delete(f"{user_id}-token")
