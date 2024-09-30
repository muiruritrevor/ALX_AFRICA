# Generated by Django 5.1 on 2024-09-27 21:10

import django.db.models.functions.text
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_genre_name_bookinstance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(help_text='Enter a brief description of the book', max_length=1000),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular book across the whole library', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('M', 'Maintenance'), ('O', 'On loan'), ('A', 'Available'), ('R', 'Reserved')], default='m', help_text='Book availability', max_length=1),
        ),
        migrations.AddConstraint(
            model_name='genre',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='genre_name_case_insensitive_unique', violation_error_message='Genre already exists (case insensitive match)'),
        ),
    ]
