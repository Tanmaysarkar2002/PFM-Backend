# Generated by Django 5.0.3 on 2024-03-24 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_alter_userinformation_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
    ]
