# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Programmer'
        db.create_table('programming_programmer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('homePhone', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('mobilePhone', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('programming', ['Programmer'])

        # Adding model 'Rating'
        db.create_table('programming_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('largeImage', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('smallImage', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('programming', ['Rating'])

        # Adding model 'Season'
        db.create_table('programming_season', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('graphic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('programmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programming.Programmer'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('programming', ['Season'])

        # Adding model 'Film'
        db.create_table('programming_film', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('length', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('director', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('certificate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programming.Rating'])),
            ('filmFormat', self.gf('django.db.models.fields.CharField')(default='UK', max_length=15)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programming.Season'])),
            ('graphic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('programmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programming.Programmer'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('programming', ['Film'])

        # Adding model 'Gig'
        db.create_table('programming_gig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('graphic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('programmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programming.Programmer'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('programming', ['Gig'])

        # Adding model 'Event'
        db.create_table('programming_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('graphic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('programmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programming.Programmer'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('programming', ['Event'])

        # Adding model 'Festival'
        db.create_table('programming_festival', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('graphic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('programmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programming.Programmer'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('programming', ['Festival'])

        # Adding M2M table for field films on 'Festival'
        db.create_table('programming_festival_films', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('festival', models.ForeignKey(orm['programming.festival'], null=False)),
            ('film', models.ForeignKey(orm['programming.film'], null=False))
        ))
        db.create_unique('programming_festival_films', ['festival_id', 'film_id'])

        # Adding M2M table for field gigs on 'Festival'
        db.create_table('programming_festival_gigs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('festival', models.ForeignKey(orm['programming.festival'], null=False)),
            ('gig', models.ForeignKey(orm['programming.gig'], null=False))
        ))
        db.create_unique('programming_festival_gigs', ['festival_id', 'gig_id'])

        # Adding M2M table for field events on 'Festival'
        db.create_table('programming_festival_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('festival', models.ForeignKey(orm['programming.festival'], null=False)),
            ('event', models.ForeignKey(orm['programming.event'], null=False))
        ))
        db.create_unique('programming_festival_events', ['festival_id', 'event_id'])

        # Adding model 'Meeting'
        db.create_table('programming_meeting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('programmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programming.Programmer'])),
        ))
        db.send_create_signal('programming', ['Meeting'])


    def backwards(self, orm):
        
        # Deleting model 'Programmer'
        db.delete_table('programming_programmer')

        # Deleting model 'Rating'
        db.delete_table('programming_rating')

        # Deleting model 'Season'
        db.delete_table('programming_season')

        # Deleting model 'Film'
        db.delete_table('programming_film')

        # Deleting model 'Gig'
        db.delete_table('programming_gig')

        # Deleting model 'Event'
        db.delete_table('programming_event')

        # Deleting model 'Festival'
        db.delete_table('programming_festival')

        # Removing M2M table for field films on 'Festival'
        db.delete_table('programming_festival_films')

        # Removing M2M table for field gigs on 'Festival'
        db.delete_table('programming_festival_gigs')

        # Removing M2M table for field events on 'Festival'
        db.delete_table('programming_festival_events')

        # Deleting model 'Meeting'
        db.delete_table('programming_meeting')


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
        'programming.event': {
            'Meta': {'ordering': "['-start']", 'object_name': 'Event'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'graphic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'programming.festival': {
            'Meta': {'ordering': "['-start']", 'object_name': 'Festival'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['programming.Event']", 'symmetrical': 'False', 'blank': 'True'}),
            'films': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['programming.Film']", 'symmetrical': 'False', 'blank': 'True'}),
            'gigs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['programming.Gig']", 'symmetrical': 'False', 'blank': 'True'}),
            'graphic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'programming.film': {
            'Meta': {'ordering': "['-start']", 'object_name': 'Film'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'certificate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Rating']"}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'filmFormat': ('django.db.models.fields.CharField', [], {'default': "'UK'", 'max_length': '15'}),
            'graphic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Season']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'programming.gig': {
            'Meta': {'ordering': "['-start']", 'object_name': 'Gig'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'graphic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'programming.meeting': {
            'Meta': {'ordering': "['-start']", 'object_name': 'Meeting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'programming.programmer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Programmer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'homePhone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobilePhone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'Meta': {'ordering': "['-start']", 'object_name': 'Season'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'graphic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming.Programmer']"}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['programming']
