# Generated by Django 5.1 on 2024-09-28 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_transaction_is_overdue_alter_book_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='publish_date',
            new_name='publication_date',
        ),
    ]
