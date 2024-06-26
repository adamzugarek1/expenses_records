# Generated by Django 4.2.9 on 2024-03-19 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')], max_length=3)),
                ('rate', models.FloatField()),
                ('date', models.DateField()),
            ],
            options={
                'unique_together': {('date', 'currency')},
            },
        ),
    ]
