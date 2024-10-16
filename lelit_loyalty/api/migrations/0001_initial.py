# Generated by Django 5.1.1 on 2024-09-23 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('lang', models.CharField(blank=True, max_length=2, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('barcode', models.CharField(blank=True, max_length=9, null=True)),
                ('birth_date', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('balance', models.IntegerField()),
            ],
        ),
    ]
