from userprofile.models import *
from rest_framework import relations
from rest_framework import *
from django.db import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id',)
        permission_classes = (permissions.IsAuthenticated,)
        

class UserProfileSerializer(serializers.RelatedField):
    def to_native(self, value):
        return value.user.username
class SubcategorySerializer(serializers.RelatedField):
    def to_native(self, value):
        return value.id

class GameInstanceSerializer(serializers.HyperlinkedModelSerializer):
    
    player1 = UserProfileSerializer()
    player2 = UserProfileSerializer()
    mode = SubcategorySerializer()
    class Meta:
        model = GameInstance
        fields = ('id','player1','player2','available','mode')
        permission_classes = (permissions.IsAuthenticated,)  

class CheckpointsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Checkpoint
        fields = ('id','latitudeP1','longitudeP1','latitudeP2','longitudeP2')
        permission_classes = (permissions.IsAuthenticated,)
        
class AcceptGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameInstance
        fields = ('winner',)
        permission_classes = (permissions.IsAuthenticated,)

