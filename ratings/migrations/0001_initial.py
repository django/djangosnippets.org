# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'RatedItem'
        db.create_table('ratings_rateditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0, db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rateditems', to=orm['auth.User'])),
            ('hashed', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rated_items', to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('ratings', ['RatedItem'])

        # Adding model 'SimilarItem'
        db.create_table('ratings_similaritem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='similar_items', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('similar_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='similar_items_set', to=orm['contenttypes.ContentType'])),
            ('similar_object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('ratings', ['SimilarItem'])

    def backwards(self, orm):

        # Deleting model 'RatedItem'
        db.delete_table('ratings_rateditem')

        # Deleting model 'SimilarItem'
        db.delete_table('ratings_similaritem')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ratings.rateditem': {
            'Meta': {'object_name': 'RatedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rated_items'", 'to': "orm['contenttypes.ContentType']"}),
            'hashed': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rateditems'", 'to': "orm['auth.User']"})
        },
        'ratings.similaritem': {
            'Meta': {'object_name': 'SimilarItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'similar_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_items_set'", 'to': "orm['contenttypes.ContentType']"}),
            'similar_object_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['ratings']
