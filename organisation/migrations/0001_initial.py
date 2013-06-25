# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Minutes'
        db.create_table('organisation_minutes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meetingType', self.gf('django.db.models.fields.CharField')(default='General Meeting', max_length=30)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('organisation', ['Minutes'])


    def backwards(self, orm):
        
        # Deleting model 'Minutes'
        db.delete_table('organisation_minutes')


    models = {
        'organisation.minutes': {
            'Meta': {'object_name': 'Minutes'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meetingType': ('django.db.models.fields.CharField', [], {'default': "'General Meeting'", 'max_length': '30'})
        }
    }

    complete_apps = ['organisation']
