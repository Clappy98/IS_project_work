# Generated by Django 4.0.4 on 2022-10-05 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_performance_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
