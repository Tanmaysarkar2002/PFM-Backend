# Generated by Django 5.0.3 on 2024-03-24 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='email',
            field=models.EmailField(default=None, max_length=200),
        ),
    ]