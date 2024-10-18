# Generated by Django 3.1.1 on 2024-08-08 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SubPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubPartRawMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_required', models.FloatField()),
                ('raw_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.rawmaterial')),
                ('sub_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.subpart')),
            ],
        ),
        migrations.AddField(
            model_name='subpart',
            name='raw_material',
            field=models.ManyToManyField(through='inventory.SubPartRawMaterial', to='inventory.RawMaterial'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sub_parts', models.ManyToManyField(to='inventory.SubPart')),
            ],
        ),
    ]
