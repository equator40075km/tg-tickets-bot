# Generated by Django 4.2 on 2023-05-27 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='msgs2delete',
            field=models.TextField(blank=True),
        ),
    ]