# Generated by Django 3.2.12 on 2022-04-17 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='purchase',
            unique_together={('property', 'user')},
        ),
    ]