# Generated by Django 5.1.4 on 2025-01-14 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_remove_status_match_in_round_index_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='matches_won',
            field=models.IntegerField(default=0),
        ),
    ]
