# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Script.hash'
        db.alter_column(u'backend_script', 'hash', self.gf('django.db.models.fields.CharField')(max_length=12, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Script.hash'
        raise RuntimeError("Cannot reverse this migration. 'Script.hash' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Script.hash'
        db.alter_column(u'backend_script', 'hash', self.gf('django.db.models.fields.CharField')(max_length=12))

    models = {
        u'backend.char': {
            'Meta': {'object_name': 'Char'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
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