from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Notification for {self.recipient.username}: {self.verb}'