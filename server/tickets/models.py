from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    text = models.TextField(blank=True)
    img_url = models.URLField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return f'{self.id}: <{self.date}> {self.title}'


class TGAdmin(models.Model):
    user_id = models.BigIntegerField()
    name = models.CharField(max_length=100)
    can_appoint = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}: {self.name}'
