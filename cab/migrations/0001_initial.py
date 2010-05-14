# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Language'
        db.create_table('cab_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('file_extension', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('cab', ['Language'])

        # Adding model 'Snippet'
        db.create_table('cab_snippet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cab.Language'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('description_html', self.gf('django.db.models.fields.TextField')()),
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('highlighted_code', self.gf('django.db.models.fields.TextField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('bookmark_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('cab', ['Snippet'])

        # Adding model 'Bookmark'
        db.create_table('cab_bookmark', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('snippet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bookmarks', to=orm['cab.Snippet'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cab_bookmarks', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('cab', ['Bookmark'])

        # Adding model 'Rating'
        db.create_table('cab_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('snippet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['cab.Snippet'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cab_ratings', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('score', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('cab', ['Rating'])


    def backwards(self, orm):
        
        # Deleting model 'Language'
        db.delete_table('cab_language')

        # Deleting model 'Snippet'
        db.delete_table('cab_snippet')

        # Deleting model 'Bookmark'
        db.delete_table('cab_bookmark')

        # Deleting model 'Rating'
        db.delete_table('cab_rating')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cab.bookmark': {
            'Meta': {'object_name': 'Bookmark'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bookmarks'", 'to': "orm['cab.Snippet']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cab_bookmarks'", 'to': "orm['auth.User']"})
        },
        'cab.language': {
            'Meta': {'object_name': 'Language'},
            'file_extension': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'cab.rating': {
            'Meta': {'object_name': 'Rating'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['cab.Snippet']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cab_ratings'", 'to': "orm['auth.User']"})
        },
        'cab.snippet': {
            'Meta': {'object_name': 'Snippet'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'bookmark_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {}),
            'highlighted_code': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cab.Language']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cab']
