
from south.db import db
from django.db import models
from ftrain.ohlih.models import *

class Migration:

    def forwards(self, orm):
        # Deleting field 'Weight.weight'
        db.delete_column('ohlih_weight', 'weight')
        db.rename_column('ohlih_weight','weight_float','weight')
    
    
    def backwards(self, orm):
        # Adding field 'Weight.weight'
        db.rename_column('ohlih_weight','weight','weight_float')
        db.add_column('ohlih_weight', 'weight', orm['ohlih.weight:weight'])
    
    models = {
        'ohlih.event': {
            'commentary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.EventType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'ohlih.weight': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.Event']"}),
            'weight_float': ('django.db.models.fields.FloatField', [], {})
        },
        'ohlih.eventtype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ohlih.energy': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kcal': ('django.db.models.fields.IntegerField', [], {}),
            'kcal_is_est': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ohlih.bloodpressure': {
            'diastolic': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.Event']"}),
            'systolic': ('django.db.models.fields.IntegerField', [], {})
        },
        'ohlih.image': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.Event']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'[notrun]'", 'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'ohlih.consumption': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.Event']"}),
            'of_energy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.Energy']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }
    
    complete_apps = ['ohlih']
