# Generated by Django 4.1 on 2022-08-14 14:25

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('men', 'Men'), ('women', 'Women')], max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('date_added',),
            },
        ),
        migrations.CreateModel(
            name='ProductStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('3', 'UK3'), ('4', 'UK4'), ('5', 'UK5'), ('6', 'UK6'), ('7', 'UK7'), ('8', 'UK8'), ('9', 'UK9'), ('10', 'UK10'), ('11', 'UK11'), ('12', 'UK12'), ('13', 'UK13'), ('14', 'UK14'), ('15', 'UK15'), ('16', 'UK16')], max_length=10)),
                ('amount_in_stock', models.IntegerField()),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_stock', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productImages', to='product.product')),
            ],
        ),
        migrations.AddConstraint(
            model_name='productstock',
            constraint=models.UniqueConstraint(fields=('product', 'size'), name='unique_prod_size_combo'),
        ),
    ]
