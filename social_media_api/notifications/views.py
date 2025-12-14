# notifications/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

# Temporary placeholder for NotificationListView
class NotificationListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "This is a placeholder for NotificationListView"})
