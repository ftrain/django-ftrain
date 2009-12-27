
from south.db import db
from django.db import models
from ftrain.ohlih.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Event'
        db.create_table('ohlih_event', (
            ('event_type', orm['ohlih.Event:event_type']),
            ('commentary', orm['ohlih.Event:commentary']),
            ('id', orm['ohlih.Event:id']),
            ('time', orm['ohlih.Event:time']),
        ))
        db.send_create_signal('ohlih', ['Event'])
        
        # Adding model 'Food'
        db.create_table('ohlih_food', (
            ('name', orm['ohlih.Food:name']),
            ('id', orm['ohlih.Food:id']),
            ('in_event', orm['ohlih.Food:in_event']),
            ('kcal_is_est', orm['ohlih.Food:kcal_is_est']),
            ('order', orm['ohlih.Food:order']),
            ('kcal', orm['ohlih.Food:kcal']),
            ('quantity', orm['ohlih.Food:quantity']),
        ))
        db.send_create_signal('ohlih', ['Food'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Event'
        db.delete_table('ohlih_event')
        
        # Deleting model 'Food'
        db.delete_table('ohlih_food')
        
    
    
    models = {
        'ohlih.event': {
            'commentary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'ohlih.food': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.Event']"}),
            'kcal': ('django.db.models.fields.IntegerField', [], {}),
            'kcal_is_est': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }
    
    complete_apps = ['ohlih']
