# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CategoryTranslation'
        db.create_table(u'aldryn_categories_category_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default=u'', max_length=255, blank=True)),
            (u'master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['aldryn_categories.Category'])),
        ))
        db.send_create_signal(u'aldryn_categories', ['CategoryTranslation'])

        # Adding unique constraint on 'CategoryTranslation', fields ['language_code', u'master']
        db.create_unique(u'aldryn_categories_category_translation', ['language_code', u'master_id'])

        # Adding model 'Category'
        db.create_table(u'aldryn_categories_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rgt', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'aldryn_categories', ['Category'])


    def backwards(self, orm):
        # Removing unique constraint on 'CategoryTranslation', fields ['language_code', u'master']
        db.delete_unique(u'aldryn_categories_category_translation', ['language_code', u'master_id'])

        # Deleting model 'CategoryTranslation'
        db.delete_table(u'aldryn_categories_category_translation')

        # Deleting model 'Category'
        db.delete_table(u'aldryn_categories_category')


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
            'Meta': {'unique_together': "[(u'language_code', u'master')]", 'object_name': 'CategoryTranslation', 'db_table': "u'aldryn_categories_category_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['aldryn_categories.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['aldryn_categories']