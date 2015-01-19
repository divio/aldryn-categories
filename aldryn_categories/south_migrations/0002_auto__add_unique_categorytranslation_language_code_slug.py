# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'CategoryTranslation', fields ['language_code', 'slug']
        db.create_unique(u'aldryn_categories_category_translation', ['language_code', 'slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'CategoryTranslation', fields ['language_code', 'slug']
        db.delete_unique(u'aldryn_categories_category_translation', ['language_code', 'slug'])


    models = {
        u'aldryn_categories.category': {
            'Meta': {'object_name': 'Category'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'aldryn_categories.categorytranslation': {
            'Meta': {'unique_together': "[(u'language_code', u'slug'), (u'language_code', u'master')]", 'object_name': 'CategoryTranslation', 'db_table': "u'aldryn_categories_category_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['aldryn_categories.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['aldryn_categories']