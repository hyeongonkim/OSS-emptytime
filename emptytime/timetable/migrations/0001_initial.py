# Generated by Django 2.2.5 on 2019-09-24 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username_text', models.CharField(max_length=8)),
                ('pw_text', models.CharField(max_length=30)),
            ],
        ),
    ]
