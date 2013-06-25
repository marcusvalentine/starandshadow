# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Picture.modified'
        db.add_column('fileupload_picture', 'modified', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 05, 11)), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Picture.modified'
        db.delete_column('fileupload_picture', 'modified')


    models = {
        'fileupload.picture': {
            'Meta': {'object_name': 'Picture'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['fileupload']
