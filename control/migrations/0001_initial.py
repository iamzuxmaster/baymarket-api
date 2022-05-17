# Generated by Django 4.0.4 on 2022-04-20 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('role', models.CharField(choices=[('client', 'Client'), ('moderator', 'Moderator-Admin'), ('admin', 'Controller'), ('superadmin', 'SuperAdmin'), ('dev', 'Developer')], default='client', max_length=255)),
                ('verified', models.BooleanField(default=False)),
                ('block', models.BooleanField(default=False)),
                ('block_end', models.DateTimeField(blank=True, null=True)),
                ('legal', models.BooleanField(default=False)),
                ('balance_id', models.IntegerField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Аккаунт',
                'verbose_name_plural': 'Аккаунты',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[600, 600], upload_to='companies/')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('verified', models.BooleanField(default=False)),
                ('address', models.TextField()),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_vierfied', models.DateTimeField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='control.account')),
            ],
            options={
                'verbose_name': 'Компание',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uz', models.CharField(max_length=255)),
                ('title_ru', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('in', 'Prixod'), ('out', 'Rasxod')], max_length=255)),
                ('sum', models.IntegerField()),
                ('pay_option', models.CharField(choices=[('click', 'Click'), ('payme', 'PayMe')], max_length=255)),
                ('pay_option_key', models.CharField(blank=True, max_length=500, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.account')),
            ],
        ),
        migrations.CreateModel(
            name='Disctrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uz', models.CharField(max_length=255)),
                ('title_ru', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.region')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Городы',
            },
        ),
        migrations.CreateModel(
            name='CompanySocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.company')),
                ('social', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='control.social')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyPhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('phone', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.company')),
            ],
        ),
    ]
