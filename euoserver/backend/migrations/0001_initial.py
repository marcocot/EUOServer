# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Char'
        db.create_table(u'backend_char', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('shard', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal(u'backend', ['Char'])

        # Adding model 'Script'
        db.create_table(u'backend_script', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('script', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'backend', ['Script'])


    def backwards(self, orm):
        # Deleting model 'Char'
        db.delete_table(u'backend_char')

        # Deleting model 'Script'
        db.delete_table(u'backend_script')


    models = {
        u'backend.char': {
            'Meta': {'object_name': 'Char'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'shard': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'backend.script': {
            'Meta': {'object_name': 'Script'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'script': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        }
    }

    complete_apps = ['backend']