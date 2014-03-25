from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Bonus(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=50)
	value = models.FloatField()
	
	def __unicode__(self):
		return self.name

class Item(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	icon = models.ImageField(upload_to = 'images/items/', default = 'item_icon.png')

	def __unicode__(self):
		return self.name

class TaskItem(Item):
	def __unicode__(self):
		return self.name

class BaseObject(Item):
	level_max = models.IntegerField()
	bonus = models.ForeignKey(Bonus)
	price_points = models.IntegerField()
	price_rock = models.IntegerField()
	price_gold = models.IntegerField()
	price_wood = models.IntegerField()

	def __unicode__(self):
		return self.name
	
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
	#count_rock = models.IntegerField()
	#count_gold = models.IntegerField()
	#count_wood = models.IntegerField()
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	tasks = models.ManyToManyField(Mission, through='Task')
	base_objects = models.ManyToManyField(BaseObject, through='UserBaseObject')
	equipment = models.ManyToManyField(Item, through='Equipment', related_name='equipment')
	avatar = models.ImageField(upload_to = 'images/avatars/', default = 'base_marker.png', blank=True)
	#base_level = models.IntegerField()
	def __unicode__(self):
		return self.user.username

class UserBaseObject(models.Model):
	user_profile = models.ForeignKey(UserProfile)
	base_object = models.ForeignKey(BaseObject)
	object_level = models.IntegerField()

class Equipment(models.Model):
	user_profile = models.ForeignKey(UserProfile, related_name='user_profile')
	items = models.ForeignKey(Item, related_name='items')

class Artifact(Item):
	number_of_part = models.IntegerField()
	bonus = models.ForeignKey(Bonus)

class PartOfArtifact(Item):
	artifact = models.ForeignKey(Artifact)

class Task(models.Model):
	user_profile = models.ForeignKey(UserProfile)
	mission = models.ForeignKey(Mission)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	timestamp = models.DateTimeField()
	def __unicode__(self):
		return self.mission.name

class Category(models.Model):
	name = models.CharField(max_length=200,unique=True)
	description = models.CharField(max_length=4000)
	def __unicode__(self):
		return self.name

class TaskPvp(models.Model):
	task_name = models.CharField(max_length=200,unique=True)9
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
