# Generated by Django 4.1.2 on 2022-11-13 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_alter_person_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='week',
            field=models.IntegerField(choices=[('0', 'saturday'), ('1', 'sunday'), ('2', 'monday'), ('3', 'tuesday'), ('4', 'thursday'), ('5', 'wednesday'), ('6', 'friday')], default='user'),
        ),
    ]
