# Generated by Django 4.1.2 on 2022-11-15 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0024_alter_expenses_date_added_alter_person_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='week',
            field=models.TextField(choices=[('5', 'saturday'), ('6', 'sunday'), ('0', 'monday'), ('1', 'tuesday'), ('2', 'wednesday'), ('3', 'thursday'), ('4', 'friday')], default='user', max_length=20),
        ),
    ]
