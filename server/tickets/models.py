from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    city = models.CharField(max_length=100)
    link = models.URLField(max_length=255)
    photo = models.CharField(max_length=255)  # photo parameter from https://core.telegram.org/bots/api#sendphoto
    text = models.TextField(blank=True)

    def __str__(self):
        return f'{self.id}: <{self.date}> {self.title}'


class TGAdmin(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    can_appoint = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id}: {self.name}'


class TGUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    city = models.CharField(max_length=100)
    last_action = models.DateField()

    def __str__(self):
        return f'{self.user_id}: {self.city}, {self.last_action}'
