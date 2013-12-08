from userprofile.models import *
from rest_framework import relations
from rest_framework import *
from django.db import models

class MissionSerializer(serializers.RelatedField):
    def to_native(self, value):
        return '%s :(%s)' % (value.name, value.description)
        
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    mission =  MissionSerializer()
    class Meta:
        model = Task
        fields = ('latitude', 'longitude','timestamp','mission' )
        permission_classes = (permissions.IsAuthenticated,)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id',)
        permission_classes = (permissions.IsAuthenticated,)        




