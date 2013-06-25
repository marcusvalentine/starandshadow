# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Film.approval'
        db.add_column('programming_film', 'approval',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organisation.Approval'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Festival.approval'
        db.add_column('programming_festival', 'approval',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organisation.Approval'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Gig.approval'
        db.add_column('programming_gig', 'approval',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organisation.Approval'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Season.approval'
        db.add_column('programming_season', 'approval',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organisation.Approval'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Event.approval'
        db.add_column('programming_event', 'approval',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organisation.Approval'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Meeting.approval'
        db.add_column('programming_meeting', 'approval',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organisation.Approval'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        if not db.dry_run:
            meetingwherewechanged = orm.Meeting.objects.get(id=326)
            approvalsetformigration = orm['organisation.ApprovalSet'](meeting=meetingwherewechanged)
            approvalsetformigration.save()
            adminuser = orm.Programmer.objects.get(id=183)
            for item in orm.Film.objects.all():
                if item.confirmedFlag:
                    ap = orm['organisation.Approval'](approvalset=approvalsetformigration, approver=adminuser)
                    ap.save()
                    item.approval = ap
                    item.save()

            for item in orm.Festival.objects.all():
                if item.confirmedFlag:
                    ap = orm['organisation.Approval'](approvalset=approvalsetformigration, approver=adminuser)
                    ap.save()
                    item.approval = ap
                    item.save()

            for item in orm.Gig.objects.all():
                if item.confirmedFlag:
                    ap = orm['organisation.Approval'](approvalset=approvalsetformigration, approver=adminuser)
                    ap.save()
                    item.approval = ap
                    item.save()

            for item in orm.Season.objects.all():
                if item.confirmedFlag:
                    ap = orm['organisation.Approval'](approvalset=approvalsetformigration, approver=adminuser)
                    ap.save()
                    item.approval = ap
                    item.save()

            for item in orm.Event.objects.all():
                if item.confirmedFlag:
                    ap = orm['organisation.Approval'](approvalset=approvalsetformigration, approver=adminuser)
                    ap.save()
                    item.approval = ap
                    item.save()

            for item in orm.Meeting.objects.all():
                ap = orm['organisation.Approval'](approvalset=approvalsetformigration, approver=adminuser)
                ap.save()
                item.approval = ap
                item.save()


    def backwards(self, orm):
        # Deleting field 'Film.approval'
        db.delete_column('programming_film', 'approval_id')

        # Deleting field 'Festival.approval'
        db.delete_column('programming_festival', 'approval_id')

        # Deleting field 'Gig.approval'
        db.delete_column('programming_gig', 'approval_id')

        # Deleting field 'Season.approval'
        db.delete_column('programming_season', 'approval_id')

        # Deleting field 'Event.approval'
        db.delete_column('programming_event', 'approval_id')

        # Deleting field 'Meeting.approval'
        db.delete_column('programming_meeting', 'approval_id')


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
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Meeting']"})
        },
        'programming.event': {
            'Meta': {'ordering': "['start']", 'object_name': 'Event'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'<p>DEFAULT PLACEHOLDER TEXT</p>'", 'blank': 'True'}),
            'confirmedFlag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.Picture']", 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NEW EVENT'", 'max_length': '150'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'programming.festival': {
            'Meta': {'ordering': "['start']", 'object_name': 'Festival'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'<p>DEFAULT PLACEHOLDER TEXT</p>'", 'blank': 'True'}),
            'confirmedFlag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['programming.Event']", 'symmetrical': 'False', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'films': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['programming.Film']", 'symmetrical': 'False', 'blank': 'True'}),
            'gigs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['programming.Gig']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.Picture']", 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NEW FESTIVAL'", 'max_length': '150'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'programming.film': {
            'Meta': {'ordering': "['start']", 'object_name': 'Film'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'<p>DEFAULT PLACEHOLDER TEXT</p>'", 'blank': 'True'}),
            'certificate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Rating']"}),
            'confirmedFlag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NEW FILM'", 'max_length': '150'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'programming.gig': {
            'Meta': {'ordering': "['start']", 'object_name': 'Gig'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'<p>DEFAULT PLACEHOLDER TEXT</p>'", 'blank': 'True'}),
            'confirmedFlag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.Picture']", 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NEW GIG'", 'max_length': '150'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'programming.meeting': {
            'Meta': {'ordering': "['start']", 'object_name': 'Meeting'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
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
            'Meta': {'ordering': "['start']", 'object_name': 'Season'},
            'approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organisation.Approval']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'<p>DEFAULT PLACEHOLDER TEXT</p>'", 'blank': 'True'}),
            'confirmedFlag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fileupload.Picture']", 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NEW SEASON'", 'max_length': '150'})
        }
    }

    complete_apps = ['programming']