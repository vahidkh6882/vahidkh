# Generated by Django 4.1.2 on 2022-11-14 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_remove_person_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='week',
            field=models.TextField(choices=[('zero', 'saturday'), ('one', 'sunday'), ('two', 'monday'), ('three', 'tuesday'), ('four', 'thursday'), ('five', 'wednesday'), ('six', 'friday')], default='user', max_length=20),
        ),
    ]