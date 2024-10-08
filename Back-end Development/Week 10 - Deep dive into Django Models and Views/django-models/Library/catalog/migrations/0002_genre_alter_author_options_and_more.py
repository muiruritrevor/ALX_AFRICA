# Generated by Django 5.1 on 2024-08-25 01:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a book genre', max_length=200, unique=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.RenameField(
            model_name='author',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, null=True, verbose_name='Died'),
        ),
        migrations.AddField(
            model_name='author',
            name='last_name',
            field=models.CharField(default='unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='book',
            name='summary',
            field=models.TextField(default='No summary available', help_text='Enter brief description of the book', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='library',
            name='location',
            field=models.CharField(default='No sumary available', help_text='Enter Location of the Library', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.author'),
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Select a genre for this book', to='catalog.genre'),
        ),
    ]
