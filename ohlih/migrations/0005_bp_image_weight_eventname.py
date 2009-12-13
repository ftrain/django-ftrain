
from south.db import db
from django.db import models
from ftrain.ohlih.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Weight'
        db.create_table('ohlih_weight', (
            ('in_event', orm['ohlih.weight:in_event']),
            ('id', orm['ohlih.weight:id']),
            ('weight', orm['ohlih.weight:weight']),
        ))
        db.send_create_signal('ohlih', ['Weight'])
        
        # Adding model 'BloodPressure'
        db.create_table('ohlih_bloodpressure', (
            ('in_event', orm['ohlih.bloodpressure:in_event']),
            ('systolic', orm['ohlih.bloodpressure:systolic']),
            ('id', orm['ohlih.bloodpressure:id']),
            ('diastolic', orm['ohlih.bloodpressure:diastolic']),
        ))
        db.send_create_signal('ohlih', ['BloodPressure'])
        
        # Adding model 'EventType'
        db.create_table('ohlih_eventtype', (
            ('id', orm['ohlih.eventtype:id']),
            ('name', orm['ohlih.eventtype:name']),
        ))
        db.send_create_signal('ohlih', ['EventType'])
        
        # Adding model 'Image'
        db.create_table('ohlih_image', (
            ('in_event', orm['ohlih.image:in_event']),
            ('original_image', orm['ohlih.image:original_image']),
            ('id', orm['ohlih.image:id']),
            ('name', orm['ohlih.image:name']),
        ))
        db.send_create_signal('ohlih', ['Image'])
        
        # Adding field 'Event.event_name'
        db.add_column('ohlih_event', 'event_name', models.ForeignKey(Event, default=0), keep_default=False)
        
    #orm['ohlih.event:event_name']
    
    
    def backwards(self, orm):
        
        # Deleting model 'Weight'
        db.delete_table('ohlih_weight')
        
        # Deleting model 'BloodPressure'
        db.delete_table('ohlih_bloodpressure')
        
        # Deleting model 'EventType'
        db.delete_table('ohlih_eventtype')
        
        # Deleting model 'Image'
        db.delete_table('ohlih_image')
        
        # Deleting field 'Event.event_name'
        db.delete_column('ohlih_event', 'event_name_id')
        
    
    
    models = {
        'ohlih.event': {
            'commentary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.EventType']"}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'ohlih.weight': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.Event']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
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
            'in_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ohlih.Event']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'[notrun]'", 'max_length': '100'}),
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
