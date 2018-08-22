from django.contrib import admin
from . import models

@admin.register(models.ChattyUser)
class ChattyUserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'unique_user_id',
        'partner',
    )

    list_display_links = (
        'id',
    )
