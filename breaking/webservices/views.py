from userprofile.models import UserProfile
from rest_framework import viewsets
from rest_framework import generics,permissions
from webservices.serializers import *
from django.utils import timezone
from django.db.models import Q
from django.db import connection
from datetime import datetime
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
        for x in queryset:
            if x.dateTime2 <= timezone.now():
                x.available=True
                x.save()
                
        return queryset
class CheckpointsViev(generics.ListAPIView):
    serializer_class = CheckpointsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        gid = self.kwargs['gid']
        queryset = Checkpoint.objects.filter(game=gid)
        return queryset
def getWinnerId(self):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT CASE (SELECT r.win  FROM (SELECT max(c.\"dateTimePlayer2\") as dt ,2 as win FROM "
                       +"userprofile_checkpoint as c WHERE game_id=1 UNION SELECT max(c.\"dateTimePlayer1\") as "
                       +"dt,1 as win FROM userprofile_checkpoint as c WHERE game_id=1)as r Order By r.dt LIMIT 1)"
                       +" WHEN 1 THEN (SELECT player1_id FROM userprofile_gameinstance WHERE id = 1) else (SELECT "
                       +"player2_id FROM userprofile_gameinstance WHERE id = 1) END ", [self,self,self,self])
        row = cursor.fetchone()
    finally:
        cursor.close()
        return row[0]

class AcceptGameViev(generics.ListAPIView):
    serializer_class = AcceptGameSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user_id= self.kwargs['player1']
        checkpoint_id= self.kwargs['cid']
        dateTime = datetime.fromtimestamp(int(self.kwargs['dt']))
        a = Checkpoint.objects.get(id=checkpoint_id)    
        game_id =a.game.id; 
        p1 = GameInstance.objects.filter((Q(player1=user_id ) & Q(id=game_id)))
        if p1 : 
            a.dateTimePlayer1 = dateTime
        else:
            a.dateTimePlayer2 = dateTime
        a.save()

        c = Checkpoint.objects.filter((Q(game=game_id ) & (Q(dateTimePlayer1__isnull = True)|Q(dateTimePlayer2__isnull = True))))


        if not c :
            game = GameInstance.objects.get(id=game_id)
            game.winner = getWinnerId(game_id)
            game.save()
            winner = UserProfile.objects.get(user_id=game.winner)
            winner.points = winner.points + game.mode.points_to_achive
            winner.save()
            
        queryset = GameInstance.objects.filter(id=game_id)
        return queryset

            
        
