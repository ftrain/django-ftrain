
from south.db import db
from django.db import models
from ftrain.ohlih.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Energy'
        db.create_table('ohlih_energy', (
            ('kcal_is_est', orm['ohlih.energy:kcal_is_est']),
            ('kcal', orm['ohlih.energy:kcal']),
            ('id', orm['ohlih.energy:id']),
            ('name', orm['ohlih.energy:name']),
        ))
        db.send_create_signal('ohlih', ['Energy'])
        
        # Adding model 'Consumption'
        db.create_table('ohlih_consumption', (
            ('in_event', orm['ohlih.consumption:in_event']),
            ('order', orm['ohlih.consumption:order']),
            ('id', orm['ohlih.consumption:id']),
            ('quantity', orm['ohlih.consumption:quantity']),
            ('of_energy', orm['ohlih.consumption:of_energy']),
        ))
        db.send_create_signal('ohlih', ['Consumption'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Energy'
        db.delete_table('ohlih_energy')
        
        # Deleting model 'Consumption'
        db.delete_table('ohlih_consumption')
        
    
    
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
        'ohlih.food': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.Event']"}),
            'kcal': ('django.db.models.fields.IntegerField', [], {}),
            'kcal_is_est': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.CharField', [], {'max_length': '10'})
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
