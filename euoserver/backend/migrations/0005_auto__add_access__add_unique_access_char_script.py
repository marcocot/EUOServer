# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Access'
        db.create_table(u'backend_access', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('char', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Char'])),
            ('script', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Script'])),
            ('expire', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'backend', ['Access'])

        # Adding unique constraint on 'Access', fields ['char', 'script']
        db.create_unique(u'backend_access', ['char_id', 'script_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Access', fields ['char', 'script']
        db.delete_unique(u'backend_access', ['char_id', 'script_id'])

        # Deleting model 'Access'
        db.delete_table(u'backend_access')


    models = {
        u'backend.access': {
            'Meta': {'unique_together': "(['char', 'script'],)", 'object_name': 'Access'},
            'char': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.Char']"}),
            'expire': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'script': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.Script']"})
        },
        u'backend.ban': {
            'Meta': {'object_name': 'Ban'},
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
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