# Generated by Django 3.1 on 2020-10-22 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orden_Tallas',
            fields=[
                ('id', models.CharField(db_column='Descripcion_talla', max_length=30, primary_key=True, serialize=False)),
                ('marca', models.IntegerField(db_column='Orden', null=True)),
            ],
            options={
                'db_table': 'Orden_Tallas',
            },
        ),
        migrations.DeleteModel(
            name='Converts',
        ),
        migrations.DeleteModel(
            name='Descarga_imagenes',
        ),
    ]
