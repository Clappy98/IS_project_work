# Generated by Django 4.0.4 on 2022-07-11 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='performancecharacteristic',
            name='value',
            field=models.CharField(max_length=30),
        ),
    ]