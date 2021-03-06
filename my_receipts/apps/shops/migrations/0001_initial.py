# Generated by Django 3.1.8 on 2021-04-23 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('address', models.TextField(blank=True, verbose_name='Address')),
                ('itn', models.PositiveBigIntegerField(default=0, verbose_name='Individual Taxpayer Number')),
                ('url', models.URLField(blank=True, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'Shop',
                'verbose_name_plural': 'Shops',
                'ordering': ('name', 'address'),
                'unique_together': {('name', 'address')},
                'index_together': {('name', 'address')},
            },
        ),
    ]
