from userprofile.models import UserProfile
from rest_framework import viewsets
from rest_framework import generics,permissions
from webservices.serializers import *




class TaskViewList(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs['id']
        queryset = Task.objects.filter(id=user_id)
        return queryset.order_by('id')
    
class LoginUser(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Task.objects.all()
    def get_queryset(self):
        user_name = self.kwargs['username']
        queryset = User.objects.filter(username=user_name)
        return queryset
