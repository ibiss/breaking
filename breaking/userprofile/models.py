from django.db import models
from django.contrib.auth.models import User

class Bonus(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=50)
	value = models.FloatField()

class Item(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	icon = models.ImageField(upload_to = 'images/items/', default = 'item_icon.png')

	#class Meta:
	#	abstract = True

	def __unicode__(self):
		return self.name

class TaskItem(Item):
	def __unicode__(self):
		return self.name

class BaseObject(Item):
	#user_profile = models.ForeignKey(UserProfile)
	level = models.IntegerField()
	bonus = models.ForeignKey(Bonus)
	price_points = models.IntegerField()
	price_rock = models.IntegerField()
	price_gold = models.IntegerField()
	price_wood = models.IntegerField()
	
class Mission(models.Model):
	name = models.CharField(max_length=100)
	marker = models.ImageField(upload_to = 'images/markers/', default = 'mission_marker.png')
	description = models.TextField()
	item_pre = models.ForeignKey(TaskItem, related_name ='item_pre')
	item_post = models.ForeignKey(TaskItem, related_name ='item_post')
	points = models.IntegerField()
	count_rock = models.IntegerField()
	count_gold = models.IntegerField()
	count_wood = models.IntegerField()
	def __unicode__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True, unique=True)
	points = models.IntegerField()
	rank_points = models.IntegerField()
	count_rock = models.IntegerField()
	count_gold = models.IntegerField()
	count_wood = models.IntegerField()
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	tasks = models.ManyToManyField(Mission, through='Task')
	avatar = models.ImageField(upload_to = 'images/avatars/', default = 'base_marker.png', blank=True)
	base_level = models.IntegerField()
	def __unicode__(self):
		return self.user.username

class Equipment(models.Model):
	user_profile = models.ForeignKey(UserProfile)
	items = models.ForeignKey(Item)

class Artifact(Item):
	#icon = models.ImageField(upload_to = '/images/items/artifacts', default = 'artifact.png')
	number_of_part = models.IntegerField()
	bonus = models.ForeignKey(Bonus)

class PartOfArtifact(Item):
	artifact = models.ForeignKey(Artifact)

class Task(models.Model):
	user = models.ForeignKey(UserProfile)
	mission = models.ForeignKey(Mission)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	timestamp = models.DateTimeField()
	def __unicode__(self):
		return self.mission
