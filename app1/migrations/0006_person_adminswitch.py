# Generated by Django 4.1.2 on 2022-11-04 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='adminswitch',
            field=models.BooleanField(default=False),
        ),
    ]
