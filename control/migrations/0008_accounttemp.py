# Generated by Django 4.0.4 on 2022-05-09 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0007_account_mobile_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
            ],
        ),
    ]