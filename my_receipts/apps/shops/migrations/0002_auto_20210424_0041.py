# Generated by Django 3.1.8 on 2021-04-23 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
    ]
