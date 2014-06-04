from django.contrib import admin
from userprofile.models import *
from django.contrib.auth.models import User

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'rank_points', )
    search_fields = ['user__username']
    list_filter = ('points', )

    def get_ordering(self, request):
        return ['user']

class MessageBoxAdmin(admin.ModelAdmin):
    list_display = ('fromUser', 'toUser', )
    search_fields = ['fromUser__user__username', 'toUser__user__username']

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('name',)

    def get_ordering(self, request):
        return ['name']

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('task_name','category','number_of_checkpoints',)
    search_fields = ['task_name']
    list_filter = ('category','number_of_checkpoints',)

    def get_ordering(self, request):
        return ['task_name']

class QueueAdmin(admin.ModelAdmin):
    list_display = ('player', 'mode', )
    search_fields = ['player__user__username']
    list_filter = ('mode',)

class GameInstanceAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'mode', 'available',)
    search_fields = ['player1__user__username']
    list_filter = ('mode',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MessageBox, MessageBoxAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Checkpoint)
admin.site.register(Queue, QueueAdmin)
admin.site.register(GameInstance, GameInstanceAdmin)
