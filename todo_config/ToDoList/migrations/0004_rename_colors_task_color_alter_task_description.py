# Generated by Django 4.1.7 on 2023-04-05 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDoList', '0003_alter_usertoken_expiry_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='colors',
            new_name='color',
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(blank=True, max_length=15000, null=True),
        ),
    ]
