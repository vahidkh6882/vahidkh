# Generated by Django 4.1.2 on 2022-11-08 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_person_adminswitch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='adminswitch',
            field=models.IntegerField(),
        ),
    ]
