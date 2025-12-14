from django.urls import path
from .views import *

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('unread/', UnreadNotificationListView.as_view(), name='unread-notification-list'),
    path('<int:notification_id>/read/', MarkNotificationAsReadView.as_view(), name='mark-notification-as-read'),
    path('read-all/', MarkAllNotificationsAsReadView.as_view(), name='mark-all-notifications-as-read'),
    path('<int:pk>/delete/', DeleteNotificationView.as_view(), name='delete-read-notifications'),
]