# Generated by Django 5.0.7 on 2024-07-20 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fighters', '0004_alter_fighter_division_alter_fighter_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='intro',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
    ]
