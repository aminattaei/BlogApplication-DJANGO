# Generated by Django 5.1.5 on 2025-01-27 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_contact_created_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'پیغام', 'verbose_name_plural': 'پیغام ها'},
        ),
        migrations.AddField(
            model_name='contact',
            name='is_answered',
            field=models.BooleanField(default=False, verbose_name='وضعیت پاسخ'),
        ),
    ]
