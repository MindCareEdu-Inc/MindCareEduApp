# Generated by Django 5.1.3 on 2024-12-20 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_estudantes', '0006_alter_address_cep_alter_address_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='address',
            unique_together={('street', 'number', 'city', 'cep')},
        ),
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.RemoveField(
            model_name='address',
            name='no_number',
        ),
    ]
