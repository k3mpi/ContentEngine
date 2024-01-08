# Generated by Django 5.0 on 2024-01-04 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_article_audiocomment_category_socialmedia_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='backgrounf_image')),
                ('theme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.theme')),
            ],
        ),
    ]
