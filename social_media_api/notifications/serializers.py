from rest_framework import serializers
from notifications.models import Notification
from accounts.serializers import CustomUserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    actor = CustomUserSerializer(read_only=True)
    target_type = serializers.SerializerMethodField()
    target_id = serializers.IntegerField(source='target_object_id', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target_type', 'target_id', 'is_read', 'timestamp']
        read_only_fields = ['id', 'actor', 'verb', 'target_type', 'target_id', 'timestamp']
    
    def get_target_type(self, obj):
        """Return the model name of the target object"""
        if obj.target_content_type:
            return obj.target_content_type.model
        return None