from __future__ import unicode_literals
from django.contrib import admin
from django.db import models


class MessageModel(models.Model):
    message_id = models.CharField(max_length=16)
    email = models.EmailField()
    snippet = models.CharField(max_length=255)

    def __str__(self):
        return self.snippet


@admin.register(MessageModel)
class MessageAdmin(admin.ModelAdmin):
    pass
