# Generated by Django 3.2 on 2022-12-09 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delights', '0002_inventory_used_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='state',
            field=models.CharField(default='no recipe', max_length=20),
        ),
    ]