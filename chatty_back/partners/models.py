from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from chatty_back.chatty_users import models as chattyuser_models


@python_2_unicode_compatible
class Partner(models.Model):

    """ Partner Model""" 

    profile_image = models.ImageField(blank=True, null=True)
    name = models.CharField(_("Name of Partner"), null=True, max_length=255)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    creator = models.ForeignKey(chattyuser_models.ChattyUser, on_delete=models.CASCADE, null=True, related_name="partners")
    


    def __str__(self):
        return self.name

    @property
    def diary_count(self):
        return self.diaries.count()
    
    @property
    def days_together(self):
        
        days_together = (timezone.now().day - self.created_at.day) + 1

        return abs(days_together)