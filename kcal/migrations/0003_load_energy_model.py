
from south.db import db
from django.db import models
from ftrain.ohlih.models import *

class Migration:
    no_dry_run = True    
    def forwards(self, orm):
        "Write your forwards migration here"

        food_dict = {}
        for food in orm.Food.objects.all():

            # Copy to consumption
            con = Consumption()

            con.in_event = Event(food.in_event.id)
            con.order = food.order
            con.quantity = food.quantity
            
            if food.name not in food_dict:
                # If no match, save a new energy row
                en = Energy()
                en.name = food.name
                en.kcal = food.kcal
                en.kcal_is_est = food.kcal_is_est
                en.save()

                food_dict[food.name] = en

            con.of_energy = food_dict[food.name]
            con.save()
            
    def backwards(self, orm):
        "Write your backwards migration here"
        for item in orm.Energy.objects.all():
            item.delete()
        for item in orm.Consumption.objects.all():
            item.delete()    
    
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
