# Generated by Django 3.0 on 2019-12-11 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0002_auto_20191211_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
    ]
