# Generated by Django 5.1 on 2024-09-30 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_alter_book_isbn_alter_transaction_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, default='No description available', max_length=1000),
        ),
    ]
