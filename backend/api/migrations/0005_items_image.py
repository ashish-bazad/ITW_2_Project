# Generated by Django 4.2.4 on 2023-10-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='image',
            field=models.ImageField(default='default.png', upload_to='item_pics'),
        ),
    ]
