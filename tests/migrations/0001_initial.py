# Generated by Django 2.2.11 on 2020-03-26 13:53

from django.db import migrations, models
import fnpdjango.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SomeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(null=True, storage=fnpdjango.storage.BofhFileSystemStorage(), upload_to='test')),
            ],
        ),
    ]
