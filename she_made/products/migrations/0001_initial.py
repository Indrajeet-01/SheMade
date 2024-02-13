# Generated by Django 5.0.2 on 2024-02-07 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('fragrances', 'Fragrances'), ('body_bath', 'Body Bath'), ('skin', 'Skin')], max_length=20)),
                ('sub_category', models.CharField(choices=[('fragrances', [('dhuni', 'Dhuni'), ('perfumes', 'Perfumes'), ('attars', 'Attars')]), ('body_bath', [('soaps', 'Soaps'), ('shower_gel', 'Shower Gel'), ('facewash', 'Face Wash'), ('shampoo', 'Shampoo'), ('conditioner', 'Conditioner')]), ('skin', [('facetoner', 'Face Toner'), ('aleo_gel', 'Aleo Gel'), ('lip_care', 'Lip Care'), ('scrubs', 'Scrubs')])], max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('content', models.CharField(blank=True, max_length=255)),
                ('stock', models.IntegerField(blank=True)),
                ('life', models.CharField(blank=True, max_length=255)),
                ('ingredients', models.TextField(blank=True, null=True)),
                ('direction_to_use', models.TextField(blank=True, null=True)),
                ('images', models.ManyToManyField(blank=True, related_name='product_items', to='products.image')),
            ],
        ),
    ]
