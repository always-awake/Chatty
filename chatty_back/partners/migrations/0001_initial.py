# Generated by Django 2.0.8 on 2018-08-22 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chatty_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name of Partner')),
                ('bio', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='chatty_users.ChattyUser')),
            ],
        ),
    ]