# Generated by Django 4.0.4 on 2022-05-13 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baymarket', '0006_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='not_verified',
            field=models.BooleanField(default=False),
        ),
    ]
