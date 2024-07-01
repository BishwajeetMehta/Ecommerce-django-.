# Generated by Django 5.0.6 on 2024-06-19 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_categories_delete_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('brand', models.CharField(default='Unknown', max_length=200)),
                ('image', models.ImageField(upload_to='images/product')),
                ('stock', models.IntegerField(default='1')),
                ('status', models.IntegerField(default='1')),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.categories')),
            ],
        ),
    ]