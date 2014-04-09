from django.contrib import admin
from userprofile.models import *

admin.site.register(UserProfile)
admin.site.register(MessageBox)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Checkpoint)
admin.site.register(Queue)
admin.site.register(GameInstance)
