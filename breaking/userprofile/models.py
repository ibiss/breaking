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

class Category(models.Model):
	name = models.CharField(max_length=200,unique=True)
	description = models.CharField(max_length=4000)
	def __unicode__(self):
		return self.name

class TaskPvp(models.Model):
	task_name = models.CharField(max_length=200,unique=True)
	description = models.CharField(max_length=4000)
	category = models.ForeignKey(Category)
	points_to_achive = models.IntegerField(validators = MinValueValidator(1))
	number_of_checkpoints = models.PositiveSmallIntegerField(validators = MinValueValidator(1))
	def __unicode__(self):
		return self.task_name

class Checkpoint(models.Model):
	takspvp = models.ForeignKey(TaskPvp)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
