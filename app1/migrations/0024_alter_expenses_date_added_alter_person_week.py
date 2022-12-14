# Generated by Django 4.1.2 on 2022-11-15 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0023_alter_expenses_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='week',
            field=models.TextField(choices=[('5', 'saturday'), ('6', 'sunday'), ('0', 'monday'), ('1', 'tuesday'), ('2', 'thursday'), ('3', 'wednesday'), ('4', 'friday')], default='user', max_length=20),
        ),
    ]
