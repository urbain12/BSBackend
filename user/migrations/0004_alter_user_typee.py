# Generated by Django 3.2.10 on 2023-01-07 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_typee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='typee',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
