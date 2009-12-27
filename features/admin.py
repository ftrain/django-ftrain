from django.contrib import admin
from django import forms
from models import *

admin.site.register(Type)
admin.site.register(Environment)
admin.site.register(Product)
admin.site.register(Feature)
admin.site.register(Commentary)


class VersionForm(forms.ModelForm):
    model = Version

admin.site.register(Version,
                    inlines = [FeatureInline],
                    form    = VersionForm,
                    )
