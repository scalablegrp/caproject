# Generated by Django 3.2.12 on 2022-04-16 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('cost', models.FloatField()),
                ('user', models.CharField(max_length=200)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='property.property')),
            ],
        ),
    ]
