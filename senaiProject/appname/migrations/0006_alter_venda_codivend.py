# Generated by Django 5.0.7 on 2024-08-01 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appname', '0005_alter_venda_codivend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='codivend',
            field=models.CharField(default='5d19bc047b', max_length=10, unique=True),
        ),
    ]
