# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Menu'
        db.create_table('content_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('linkText', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('content', ['Menu'])

        # Adding model 'Page'
        db.create_table('content_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('linkText', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Menu'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('content', ['Page'])

        # Adding model 'News'
        db.create_table('content_news', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('graphic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('publishDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('withdrawDate', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('content', ['News'])

        # Adding model 'Document'
        db.create_table('content_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('created', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.CharField')(default='GEN', max_length=15)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('content', ['Document'])


    def backwards(self, orm):
        
        # Deleting model 'Menu'
        db.delete_table('content_menu')

        # Deleting model 'Page'
        db.delete_table('content_page')

        # Deleting model 'News'
        db.delete_table('content_news')

        # Deleting model 'Document'
        db.delete_table('content_document')


    models = {
        'content.document': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Document'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'GEN'", 'max_length': '15'})
        },
        'content.menu': {
            'Meta': {'ordering': "['title']", 'object_name': 'Menu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkText': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'content.news': {
            'Meta': {'ordering': "['-publishDate']", 'object_name': 'News'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'graphic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publishDate': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'withdrawDate': ('django.db.models.fields.DateTimeField', [], {})
        },
        'content.page': {
            'Meta': {'ordering': "['order']", 'object_name': 'Page'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkText': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Menu']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['content']
