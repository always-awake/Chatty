from django.contrib import admin
from . import models


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'days_together',
        'diary_count',
        'creator',
    )    