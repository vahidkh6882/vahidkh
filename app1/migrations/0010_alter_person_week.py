# Generated by Django 4.1.2 on 2022-11-13 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_person_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='week',
            field=models.CharField(choices=[('vah', 'شنبه'), ('rez', 'یکشنبه')], default='user', max_length=25),
        ),
    ]
