# Generated by Django 4.1.5 on 2023-02-06 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_productstock_amount_in_stock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productstock',
            options={'ordering': ('size',)},
        ),
        migrations.AlterField(
            model_name='productstock',
            name='size',
            field=models.CharField(choices=[(3, 'UK3'), (4, 'UK4'), (5, 'UK5'), (6, 'UK6'), (7, 'UK7'), (8, 'UK8'), (9, 'UK9'), (10, 'UK10'), (11, 'UK11'), (12, 'UK12'), (13, 'UK13'), (14, 'UK14'), (15, 'UK15'), (16, 'UK16')], max_length=10),
        ),
    ]