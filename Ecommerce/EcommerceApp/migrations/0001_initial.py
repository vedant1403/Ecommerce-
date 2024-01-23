# Generated by Django 5.0 on 2023-12-28 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('wid', models.IntegerField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('mobile', 'mobile'), ('watches', 'watches'), ('laptop', 'laptop')], max_length=50)),
                ('image', models.ImageField(upload_to='pics')),
                ('description', models.CharField(max_length=250)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
