# Generated by Django 4.0.4 on 2022-10-04 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_attribute_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='name',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
