# Generated by Django 3.2 on 2022-12-09 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delights', '0005_menuitem_handwork_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='state',
        ),
    ]
