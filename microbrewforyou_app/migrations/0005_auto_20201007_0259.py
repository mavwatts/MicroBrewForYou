# Generated by Django 3.1.2 on 2020-10-07 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microbrewforyou_app', '0004_remove_customuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.TextField(choices=[('Columbus', 'Columbus'), ('Colorado springs', 'Colorado Springs'), ('Carmel', 'Carmel')], max_length=240),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='state',
            field=models.TextField(choices=[('Columbus', 'Columbus'), ('Colorado springs', 'Colorado Springs'), ('Carmel', 'Carmel')], max_length=240),
        ),
    ]
