from userprofile.models import *
from rest_framework import relations
from rest_framework import *
from django.db import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id',)
        permission_classes = (permissions.IsAuthenticated,)        




