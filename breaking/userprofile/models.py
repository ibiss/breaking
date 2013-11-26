from django.db import models
from django.contrib.auth.models import User

class Mission(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	def __unicode__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True, unique=True)
	first_name = models.CharField(max_length=100)
	second_name = models.CharField(max_length=100)
	status = models.BooleanField(default=True)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	timestamp = models.DateTimeField()
	tasks = models.ManyToManyField(Mission, through='Task')
	def __unicode__(self):
		return self.user
	
class Item(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	user = models.ForeignKey('UserProfile', related_name='items')
	def __unicode__(self):
		return self.name

class Task(models.Model):
	user = models.ForeignKey(UserProfile)
	mission = models.ForeignKey(Mission)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	timestamp = models.DateTimeField()
	def __unicode__(self):
		return self.mission
'''
class Reward(models.Model):
	name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name

class Team(models.Model):
 #	chat_id = models.ForeignKey(Chat)
	name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name
    
class UserTeam(models.Model):
	team_id = models.ForeignKey(Team)
	user_id = models.ForeignKey(UserProfile)
	status = models.IntegerField()
'''
