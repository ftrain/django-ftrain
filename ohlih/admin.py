from django import forms
from django.contrib import admin

from models import *

class ConsumptionAdmin(admin.ModelAdmin):
    search_fields = ('quantity','of_energy',)
    order = 'of_energy'
    list_display = ['in_event','of_energy','quantity','order',]

    fieldsets = (
        (None, {
            'fields': ('in_event','of_energy','quantity','order',)
        }),
    )

class EnergyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display_links = ('display',)
    list_display = ('display','name','kcal','kcal_is_est',)
    list_editable = ('name','kcal','kcal_is_est')


class ConsumptionInline(admin.TabularInline):
    model = Consumption
    extra = 3

class BloodPressureInline(admin.StackedInline):
    model = BloodPressure
    extra = 1

class WeightInline(admin.StackedInline):
    model = Weight
    extra = 1

class ImageInline(admin.StackedInline):
    model = Image
    extra = 1

class EventForm(forms.ModelForm):
    model = Event

class EventAdmin(admin.ModelAdmin):
    list_per_page = 200
    search_fields = ('commentary',)
    list_filter = ('event_name','time',)
    save_on_top = True

    inlines = [ConsumptionInline, ImageInline, BloodPressureInline, WeightInline]
    form = EventForm

admin.site.register(Event,EventAdmin)
admin.site.register(EventType)
admin.site.register(Consumption,ConsumptionAdmin)
admin.site.register(Energy,EnergyAdmin)
admin.site.register(BloodPressure)
admin.site.register(Weight)
admin.site.register(Image)



