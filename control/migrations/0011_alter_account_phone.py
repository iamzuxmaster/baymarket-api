# Generated by Django 4.0.4 on 2022-05-10 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0010_accounttemp_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]