# Generated by Django 5.1.3 on 2024-11-27 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_estudantes', '0003_alter_emocoes_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emocoes',
            name='foto',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='estudante',
            name='foto',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
