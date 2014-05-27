# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True, unique=True, verbose_name="Użytkownik")
	points = models.IntegerField(verbose_name="Punkty")
	rank_points = models.IntegerField(verbose_name="Punkty w rankingu")
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	avatar = models.ImageField(upload_to = 'images/avatars/', default = 'base_marker.png', blank=True)
	def __unicode__(self):
		return self.user.username

	class Meta:
		verbose_name = "Profil użytkownika"
		verbose_name_plural = "Profile użytkowników"

class MessageBox(models.Model):
	fromUser = models.ForeignKey(UserProfile, related_name ='fromUser', verbose_name="Adresat")
	toUser = models.ForeignKey(UserProfile, related_name ='toUser', verbose_name="Odbiorca")
	title = models.CharField(max_length=500, verbose_name='Tytuł')
	description = models.TextField(verbose_name="Treść")

	class Meta:
		verbose_name = "Skrzynka pocztowa"
		verbose_name_plural = "Skrzynka"

class Category(models.Model):
	name = models.CharField(max_length=200, unique=True, verbose_name="Nazwa kategorii")
	description = models.CharField(max_length=4000, verbose_name="Opis")
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Kategoria"
		verbose_name_plural = "Kategorie"

class Subcategory(models.Model):
	task_name = models.CharField(max_length=200, unique=True, verbose_name="Nazwa zadania")
	description = models.CharField(max_length=4000, verbose_name="Opis zadania")
	category = models.ForeignKey(Category, verbose_name="Kategoria")
	points_to_achive = models.IntegerField(verbose_name="Punkty do zdobycia")
	number_of_checkpoints = models.IntegerField(verbose_name="Ile punktów kontrolnych")
	def __unicode__(self):
		return self.task_name

	class Meta:
		verbose_name = "Szczegółowa kategoria"
		verbose_name_plural = "Szczegółowe kategorie"

class Queue(models.Model): #queueing player for create game
	player = models.ForeignKey(UserProfile, verbose_name="Użytkownik")
	mode = models.ForeignKey(Subcategory, verbose_name="Typ gry")
	timeStart = models.IntegerField(verbose_name="Początek przediału czasowego")
	timeEnd = models.IntegerField(verbose_name="Koniec przedziału czasowego")

	def __unicode__(self):
		return str(self.player) + " " + str(self.mode)

	class Meta:
		verbose_name = "Kolejka"
		verbose_name_plural = "Kolejka"

class GameInstance(models.Model): #model of game
	player1 = models.ForeignKey(UserProfile, related_name='player1', verbose_name="Gracz")
	player2 = models.ForeignKey(UserProfile, related_name='player2', verbose_name="Gracz")
	dateTime1 = models.DateTimeField(verbose_name="Czas pierwszego gracza")
	dateTime2 = models.DateTimeField(verbose_name="Czas kiedy graczom zostaną udostępnione punkty kontrolne")
	available = models.BooleanField(verbose_name="Czy gra się toczy?")
	mode = models.ForeignKey(Subcategory, verbose_name="Typ gry")
	winner = models.IntegerField(default=0,verbose_name="Zwycięzca")

	def __unicode__(self):
		return str(self.player1) + " " + str(self.player2) + " " + str(self.mode)

	class Meta:
		verbose_name = "Instancja gry"
		verbose_name_plural = "Instancje gier"

class Checkpoint(models.Model):
	game = models.ForeignKey(GameInstance)
	latitudeP1 = models.CharField(max_length=50)
	longitudeP1 = models.CharField(max_length=50)
	latitudeP2 = models.CharField(max_length=50)
	longitudeP2 = models.CharField(max_length=50)
	timePlayer1 = models.DateTimeField()
	timePlayer2 = models.DateTimeField()

	def __unicode__(self):
		return str(self.game)

	class Meta:
		verbose_name = "Punkt kontrolny"
		verbose_name_plural = "Punkty kontrolne"
