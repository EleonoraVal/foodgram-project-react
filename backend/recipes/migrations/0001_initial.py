# Generated by Django 2.2.19 on 2022-03-17 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True, unique=True)),
                ('amount', models.IntegerField(default=0)),
                ('unit', models.TextField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True, unique=True)),
                ('color', models.CharField(blank=True, default='0000FF', max_length=6, null=True)),
                ('slug', models.SlugField(max_length=30, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/')),
                ('cooking_time', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
                ('ingredient', models.ManyToManyField(related_name='recipes', to='recipes.Ingredient')),
                ('tag', models.ManyToManyField(related_name='recipes', to='recipes.Tag')),
            ],
        ),
    ]
