# Generated by Django 3.1 on 2020-09-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Converts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Descarga',
            fields=[
                ('ean', models.CharField(blank=True, db_column='EAN', max_length=30, primary_key=True, serialize=False)),
                ('imagen_grande', models.TextField(blank=True, db_column='IMAGEN_GRANDE', null=True)),
            ],
        ),
    ]
