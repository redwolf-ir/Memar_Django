# Generated by Django 3.1.1 on 2020-09-28 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shots', '0005_auto_20200928_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shot',
            name='published',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
