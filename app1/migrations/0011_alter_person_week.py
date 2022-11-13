# Generated by Django 4.1.2 on 2022-11-13 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_alter_person_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='week',
            field=models.CharField(choices=[('0', 'شنبه'), ('1', 'یکشنبه'), ('2', 'دوشنبه'), ('3', 'سه شنبه'), ('4', 'چهارشنبه'), ('5', 'پنجشنبه'), ('6', 'جمعه')], default='user', max_length=25),
        ),
    ]
