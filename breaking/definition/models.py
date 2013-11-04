from django.db import models
from django.contrib.auth.models import User

class Base(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    def __unicode_(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    base_id = models.ForeignKey(Base,null=True)
    def __unicode_(self):
        return self.user

#class Message(models.Model):
#    author_id = models.ForeignKey(UserProfile)
#    recipient_id = models.ForeignKey(UserProfile)
#    messages = models.CharField(max_length=100)
#    date_time = models.DateField(max_length=100)
#    def __unicode_(self):
#        return self

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=8000)
    def __unicode_(self):
        return self.name
    
class UserEquipment(models.Model):
    missions_id = models.ForeignKey(Item)
    user_id = models.ForeignKey(UserProfile)
    status = models.IntegerField()
    def __unicode_(self):
        return self

class Reward(models.Model):
    name = models.CharField(max_length=100)
    def __unicode_(self):
        return self.name
    
class Rewards(models.Model):
    reward_id = models.ForeignKey(Reward)
    item_id = models.ForeignKey(Item)
    quantity = models.IntegerField()
    def __unicode_(self):
        return self    
    
class Mission(models.Model):
    rewards_id = models.ForeignKey(Rewards)
    name = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    description = models.CharField(max_length=8000)
    def __unicode_(self):
        return self.name
    
class UserMission(models.Model):
    missions_id = models.ForeignKey(Mission)
    user_id = models.ForeignKey(UserProfile)
    status = models.IntegerField()
    def __unicode_(self):
        return self

class Chat(models.Model):
    author_id = models.ForeignKey(UserProfile)
    messages = models.CharField(max_length=100)
    date_time = models.DateField(max_length=100)
    def __unicode_(self):
        return self

class Team(models.Model):
    chat_id = models.ForeignKey(Chat)
    name = models.CharField(max_length=100)
    def __unicode_(self):
        return self.name
    
class UserTeam(models.Model):
    team_id = models.ForeignKey(Team)
    user_id = models.ForeignKey(UserProfile)
    status = models.IntegerField()
    def __unicode_(self):
        return self
