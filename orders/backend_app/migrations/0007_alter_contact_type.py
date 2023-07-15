# Generated by Django 4.2.2 on 2023-07-14 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0006_alter_contact_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='type',
            field=models.CharField(choices=[('supplier', 'Поставщик'), ('shop', 'Магазин')], default='shop', max_length=10, verbose_name='Тип контакта'),
        ),
    ]