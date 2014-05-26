from django.contrib import admin
from userprofile.models import *
from django.contrib.auth.models import User

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_filter = ('points',)

    def get_ordering(self, request):
        return ['user']

class MessageBoxAdmin(admin.ModelAdmin):
    def get_ordering(self, request):
        return 

class CategoryAdmin(admin.ModelAdmin):
    def get_ordering(self, request):
        return ['name']

class SubcategoryAdmin(admin.ModelAdmin):
    def get_ordering(self, request):
        return ['task_name']

class CheckpointAdmin(admin.ModelAdmin):
    def get_ordering(self, request):
        return

class QueueAdmin(admin.ModelAdmin):
    def get_ordering(self, request):
        return

class GameInstanceAdmin(admin.ModelAdmin):
    def get_ordering(self, request):
        return

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MessageBox)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Checkpoint)
admin.site.register(Queue)
admin.site.register(GameInstance)
