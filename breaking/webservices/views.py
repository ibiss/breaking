from userprofile.models import UserProfile
from rest_framework import viewsets
from rest_framework import generics,permissions
from webservices.serializers import *

class LoginUser(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user_name = self.kwargs['username']
        queryset = User.objects.filter(username=user_name)
        return queryset

class GameInstanceViev(generics.ListAPIView):
    serializer_class = GameInstanceSer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user_name = self.kwargs['player1']
        return queryset
class CheckpointsViev(generics.ListAPIView):
    serializer_class = CheckpointsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        gid = self.kwargs['gid']
        queryset = Checkpoint.objects.filter(game=gid)
        return queryset
