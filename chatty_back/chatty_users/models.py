from django.db import models



class ChattyUser(models.Model):

    """ Chatty User Model """

    name = models.CharField(null=True, max_length=80)
    unique_user_id = models.CharField(null=True, max_length=40)
    partner = models.ForeignKey('partners.Partner', on_delete=models.CASCADE, related_name="partner", null=True, blank=True)


    def __str__(self):
        return self.name