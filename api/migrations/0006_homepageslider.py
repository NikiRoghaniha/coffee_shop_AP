# Generated by Django 3.2.25 on 2024-07-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_order_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.IntegerField(unique=True)),
                ('image', models.ImageField(upload_to='')),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
