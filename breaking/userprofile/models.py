from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, primary_key=True, unique=True)
	points = models.IntegerField()
	rank_points = models.IntegerField()
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	avatar = models.ImageField(upload_to = 'images/avatars/', default = 'base_marker.png', blank=True)
	def __unicode__(self):
		return self.user.username

class MessageBox(models.Model):
	id = models.AutoField(primary_key=True)
	fromUser = models.ForeignKey(UserProfile, related_name ='fromUser')
	toUser = models.ForeignKey(UserProfile, related_name ='toUser')
	title = models.CharField(max_length=500)
	description = models.TextField()

class Category(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200,unique=True)
	description = models.CharField(max_length=4000)
	def __unicode__(self):
		return self.name

class Subcategory(models.Model):
	id = models.AutoField(primary_key=True)
	task_name = models.CharField(max_length=200,unique=True)
	description = models.CharField(max_length=4000)
	category = models.ForeignKey(Category)
	points_to_achive = models.IntegerField()
	number_of_checkpoints = models.IntegerField()
	def __unicode__(self):
		return self.task_name

class Queue(models.Model): #queueing player for create game
	player = models.ForeignKey(UserProfile)
	mode = models.ForeignKey(Subcategory)

class GameInstance(models.Model): #model of game
	id = models.AutoField(primary_key=True)
	player1 = models.ForeignKey(UserProfile, related_name='player1')
	player2 = models.ForeignKey(UserProfile, related_name='player2')
	dateTime1 = models.DateTimeField()
	dateTime2 = models.DateTimeField()
	available = models.BooleanField()
	mode = models.ForeignKey(Subcategory)
	winner = models.IntegerField(default=0)

class Checkpoint(models.Model):
	game = models.ForeignKey(GameInstance)
	latitudeP1 = models.CharField(max_length=50)
	longitudeP1 = models.CharField(max_length=50)
	latitudeP2 = models.CharField(max_length=50)
	longitudeP2 = models.CharField(max_length=50)