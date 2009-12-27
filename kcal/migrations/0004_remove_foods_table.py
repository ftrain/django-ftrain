
from south.db import db
from django.db import models
from ftrain.ohlih.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting model 'food'
        db.delete_table('ohlih_food')
        
    
    
    def backwards(self, orm):
        
        # Adding model 'food'
        db.create_table('ohlih_food', (
            ('name', orm['ohlih.food:name']),
            ('id', orm['ohlih.food:id']),
            ('in_event', orm['ohlih.food:in_event']),
            ('kcal_is_est', orm['ohlih.food:kcal_is_est']),
            ('kcal', orm['ohlih.food:kcal']),
            ('order', orm['ohlih.food:order']),
            ('quantity', orm['ohlih.food:quantity']),
        ))
        db.send_create_signal('ohlih', ['food'])
        
    
    
    models = {
        'ohlih.event': {
            'commentary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'ohlih.energy': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kcal': ('django.db.models.fields.IntegerField', [], {}),
            'kcal_is_est': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
