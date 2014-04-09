from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True, unique=True)
	points = models.IntegerField()
	rank_points = models.IntegerField()
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	avatar = models.ImageField(upload_to = 'images/avatars/', default = 'base_marker.png', blank=True)
	def __unicode__(self):
		return self.user.username

class Communicator(models.Model):
	user_profile = models.ForeignKey(UserProfile, related_name ='user_profile_c')
	user_addressee = models.ForeignKey(UserProfile, related_name ='user_addressee_c')
	description = models.TextField()

class Category(models.Model):
	name = models.CharField(max_length=200,unique=True)
	description = models.CharField(max_length=4000)
	def __unicode__(self):
		return self.name

class TaskPvp(models.Model):
	task_name = models.CharField(max_length=200,unique=True)
	description = models.CharField(max_length=4000)
	category = models.ForeignKey(Category)
	points_to_achive = models.IntegerField()
	number_of_checkpoints = models.IntegerField()
	def __unicode__(self):
		return self.task_name

class Checkpoint(models.Model):
	takspvp = models.ForeignKey(GamePVP)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)

class JoinPVP(models.Model): #queueing player for create game
	player = models.ForeignKey(UserProfile)
	mode = models.ForeignKey(TaskPvp)

class GamePVP(models.Model): #model of game
	player1 = models.ForeignKey('UserProfile', related_name='player1')
	player2 = models.ForeignKey('UserProfile', related_name='player2')
	dateTime1 = models.DateTimeField()
	dateTime2 = models.DateTimeField()
	available = models.BooleanField()
	mode = models.ForeignKey(TaskPvp)
	winner = models.IntegerField(default=0)