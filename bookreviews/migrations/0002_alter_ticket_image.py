# Generated by Django 3.2 on 2021-04-29 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookreviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
