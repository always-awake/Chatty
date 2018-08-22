from django.db import models


class ChattyUser(models.Model):

    """ Chatty User Model """

    name = models.CharField(null=True, max_length=80)
    unique_user_id = models.CharField(null=True, max_length=40)

    def __str__(self):
        return self.name