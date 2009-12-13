
from south.db import db
from django.db import models
from ftrain.ohlih.models import *

class Migration:
    no_dry_run = True        

    def forwards(self, orm):
        "Write your forwards migration here"

        event_dict = {}

        for event in orm.Event.objects.all():

            if event.event_type not in event_dict:
                # If no match, save a new energy row
                typ = EventType()
                typ.name = event.event_type
                typ.save()

                event_dict[event.event_type] = typ

            event.event_name_id = event_dict[event.event_type].id
            event.save()
    
    def backwards(self, orm):
        "Write your backwards migration here"
        for event_type in orm.EventType.objects.all():    
            event_type.delete()
    
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
