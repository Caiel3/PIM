# Generated by Django 3.1 on 2020-11-09 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0006_auto_20201106_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='materiales',
            name='tipo_material',
            field=models.TextField(blank=True, db_column='TIPO_MATERIAL', null=True),
        ),
    ]