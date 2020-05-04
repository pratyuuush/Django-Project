# Generated by Django 3.0.5 on 2020-05-03 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import imagekit.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, default='default.jpg', null=True, upload_to='profile_pics')),
                ('bio', models.CharField(blank=True, default=' ', max_length=200, null=True)),
                ('email', models.EmailField(max_length=70)),
                ('ac_type', models.CharField(choices=[('Individual', 'Individual'), ('Organization', 'Organization')], default=' ', max_length=12)),
                ('address1', models.CharField(default=' ', max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(default=' ', max_length=1024, verbose_name='Address line 2')),
                ('zip_code', models.CharField(default=' ', max_length=10, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(default=' ', max_length=1024)),
                ('state', models.CharField(default=' ', max_length=1024)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_something', models.TextField(max_length=1000, null=True)),
                ('posted_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_type', models.CharField(choices=[('Job Post', 'Job'), ('Blog Post', 'Blog')], max_length=9)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('follow_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
