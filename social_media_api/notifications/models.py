from django.db import models

# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    target = models.GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)