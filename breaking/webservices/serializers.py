from userprofile.models import *
from rest_framework import relations
from rest_framework import *
from django.db import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id',)
        permission_classes = (permissions.IsAuthenticated,)

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        user = UserSerializer()
        fields = ('user',)
        permission_classes = (permissions.IsAuthenticated,)

class SubcategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('task_name','description','points_to_achive','number_of_checkpoints')
        permission_classes = (permissions.IsAuthenticated,)

class GameInstanceSer(serializers.HyperlinkedModelSerializer):
    
    player1 = UserProfileSerializer()
    player2 = UserProfileSerializer()
    mode = SubcategorySerializer()
    class Meta:
        model = GameInstance
        fields = ('id','player1','player2','dateTime1', 'dateTime2','available' 
	,'mode','winner')
        permission_classes = (permissions.IsAuthenticated,)  




