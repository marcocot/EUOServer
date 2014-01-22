# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Char.char_id'
        db.add_column(u'backend_char', 'char_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=6),
                      keep_default=False)

        # Adding field 'Char.public_key'
        db.add_column(u'backend_char', 'public_key',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Char.char_id'
        db.delete_column(u'backend_char', 'char_id')

        # Deleting field 'Char.public_key'
        db.delete_column(u'backend_char', 'public_key')


    models = {
        u'backend.char': {
            'Meta': {'object_name': 'Char'},
            'char_id': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'public_key': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'shard': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'backend.script': {
            'Meta': {'object_name': 'Script'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'script': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        }
    }

    complete_apps = ['backend']