# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorisedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, verbose_name='Name', max_length=100)),
                ('slug', models.SlugField(unique=True, verbose_name='Slug', max_length=100)),
                ('lft', models.PositiveIntegerField(db_index=True)),
                ('rgt', models.PositiveIntegerField(db_index=True)),
                ('tree_id', models.PositiveIntegerField(db_index=True)),
                ('depth', models.PositiveIntegerField(db_index=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='categoriseditem',
            name='category',
            field=models.ForeignKey(to='aldryn_categories.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categoriseditem',
            name='content_type',
            field=models.ForeignKey(verbose_name='Content type', to='contenttypes.ContentType', related_name='aldryn_categories_categoriseditem_tagged_items'),
            preserve_default=True,
        ),
    ]
