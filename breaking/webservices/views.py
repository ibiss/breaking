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
    serializer_class = GameInstanceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user_name = self.kwargs['player1']
        queryset = GameInstance.objects.filter(player1=user_name)|GameInstance.objects.filter(player2=user_name)
        return queryset
class CheckpointsViev(generics.ListAPIView):
    serializer_class = CheckpointsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        gid = self.kwargs['gid']
        queryset = Checkpoint.objects.filter(game=gid)
        return queryset
    
class AcceptGameViev(generics.ListAPIView):
    serializer_class = AcceptGameSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user_id= self.kwargs['player1']
        queryset = GameInstance.objects.filter(player1=user_id)|GameInstance.objects.filter(player2=user_id)
        
        if queryset[0].winner==0:
            a = GameInstance.objects.get(id=queryset[0].id)
            a.winner = queryset[0].id
            a.save()
            queryset = GameInstance.objects.filter(player1=user_id)|GameInstance.objects.filter(player2=user_id)        
            return queryset
        else:
            return queryset
            
        
