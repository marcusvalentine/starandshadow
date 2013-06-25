# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Film.start'
        db.delete_column('programming_film', 'start')

        # Deleting field 'Festival.end'
        db.delete_column('programming_festival', 'end')

        # Deleting field 'Festival.start'
        db.delete_column('programming_festival', 'start')

        # Deleting field 'Gig.end'
        db.delete_column('programming_gig', 'end')

        # Deleting field 'Gig.start'
        db.delete_column('programming_gig', 'start')

        # Deleting field 'Season.end'
        db.delete_column('programming_season', 'end')

        # Deleting field 'Season.start'
        db.delete_column('programming_season', 'start')

        # Deleting field 'Event.end'
        db.delete_column('programming_event', 'end')

        # Deleting field 'Event.start'
        db.delete_column('programming_event', 'start')

        # Deleting field 'Meeting.start'
        db.delete_column('programming_meeting', 'start')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Film.start'
        raise RuntimeError("Cannot reverse this migration. 'Film.start' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Festival.end'
        raise RuntimeError("Cannot reverse this migration. 'Festival.end' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Festival.start'
        raise RuntimeError("Cannot reverse this migration. 'Festival.start' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Gig.end'
        raise RuntimeError("Cannot reverse this migration. 'Gig.end' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Gig.start'
        raise RuntimeError("Cannot reverse this migration. 'Gig.start' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Season.end'
        raise RuntimeError("Cannot reverse this migration. 'Season.end' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Season.start'
        raise RuntimeError("Cannot reverse this migration. 'Season.start' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Event.end'
        raise RuntimeError("Cannot reverse this migration. 'Event.end' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Event.start'
        raise RuntimeError("Cannot reverse this migration. 'Event.start' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Meeting.start'
        raise RuntimeError("Cannot reverse this migration. 'Meeting.start' and its values cannot be restored.")

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fileupload.picture': {
            'Meta': {'object_name': 'Picture'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'blank': 'True'})
        },
        'organisation.approval': {
            'Meta': {'object_name': 'Approval'},
            'approvalset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.ApprovalSet']"}),
            'approver': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organisation.approvalset': {
            'Meta': {'object_name': 'ApprovalSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['programming.Meeting']", 'unique': 'True'})
        },
        'programming.event': {
            'Meta': {'ordering': "['startDate', 'startTime']", 'object_name': 'Event'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'<p>DEFAULT PLACEHOLDER TEXT</p>'", 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'endTime': ('django.db.models.fields.TimeField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.Picture']", 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.TimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NEW EVENT'", 'max_length': '150'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'programming.festival': {
            'Meta': {'ordering': "['startDate', 'startTime']", 'object_name': 'Festival'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'<p>DEFAULT PLACEHOLDER TEXT</p>'", 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'endDate': ('django.db.models.fields.DateField', [], {}),
            'endTime': ('django.db.models.fields.TimeField', [], {}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['programming.Event']", 'symmetrical': 'False', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'films': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['programming.Film']", 'symmetrical': 'False', 'blank': 'True'}),
            'gigs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['programming.Gig']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.Picture']", 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.TimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NEW FESTIVAL'", 'max_length': '150'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'programming.film': {
            'Meta': {'ordering': "['startDate', 'startTime']", 'object_name': 'Film'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'<p>DEFAULT PLACEHOLDER TEXT</p>'", 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'certificate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Rating']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filmFormat': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.Picture']", 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Season']"}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.TimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NEW FILM'", 'max_length': '150'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'programming.gig': {
            'Meta': {'ordering': "['startDate', 'startTime']", 'object_name': 'Gig'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'<p>DEFAULT PLACEHOLDER TEXT</p>'", 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'endTime': ('django.db.models.fields.TimeField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.Picture']", 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.TimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NEW GIG'", 'max_length': '150'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'programming.meeting': {
            'Meta': {'ordering': "['startDate', 'startTime']", 'object_name': 'Meeting'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'General Meeting'", 'max_length': '150'})
        },
        'programming.programmer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Programmer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'homePhone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobilePhone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'default': "'img/programmer/ron1-small.jpg'", 'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'programming.rating': {
            'Meta': {'ordering': "['name']", 'object_name': 'Rating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'largeImage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'smallImage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'programming.season': {
            'Meta': {'ordering': "['startDate']", 'object_name': 'Season'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'<p>DEFAULT PLACEHOLDER TEXT</p>'", 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'endDate': ('django.db.models.fields.DateField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.Picture']", 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NEW SEASON'", 'max_length': '150'})
        }
    }

    complete_apps = ['programming']