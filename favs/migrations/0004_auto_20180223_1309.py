# Generated by Django 2.0.2 on 2018-02-23 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_django', '0008_partial_timestamp'),
        ('favs', '0003_fav'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_id', models.CharField(max_length=128)),
                ('text', models.CharField(blank=True, max_length=500)),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_django.UserSocialAuth')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='fav',
            name='text',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
