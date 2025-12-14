from django.contrib.contenttypes.models import ContentType
from .models import Notification


def create_notification(recipient, actor, verb, target=None):
    """
    Create a notification for a user action.
    
    Args:
        recipient: The user who will receive the notification
        actor: The user who performed the action
        verb: Description of the action (e.g., "followed you", "liked your post")
        target: Optional target object (e.g., Post, Comment)
    """
    # Don't create notification if actor is the recipient
    if recipient == actor:
        return None
    
    notification_data = {
        'recipient': recipient,
        'actor': actor,
        'verb': verb,
    }
    
    if target:
        notification_data['target_content_type'] = ContentType.objects.get_for_model(target)
        notification_data['target_object_id'] = target.id
    
    return Notification.objects.create(**notification_data)
