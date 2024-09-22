# Generated by Django 5.0.3 on 2024-03-16 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('craftapp', '0002_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('PL', 'Paper Craft'), ('HD', 'Home decor'), ('DD', 'Diyas'), ('LI', 'Lighting'), ('SK', 'Sketch'), ('Cl', 'Clay art'), ('HM', 'Handicraft')], max_length=2),
        ),
    ]
