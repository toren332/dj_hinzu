# Generated by Django 3.0.6 on 2020-05-22 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_image_vector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='movies/'),
        ),
    ]