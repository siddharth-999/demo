# Generated by Django 3.2 on 2021-04-13 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0002_auto_20210413_1613'),
    ]

    operations = [
        migrations.RenameField(
            model_name='familyrelation',
            old_name='member',
            new_name='added_by',
        ),
    ]
