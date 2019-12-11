from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=True)
    body = models.CharField(max_length=255)

    def __str__(self):
        return self.title
