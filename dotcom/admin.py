from django.contrib import admin

from ftrain.dotcom.models import Link, Post, Person, By
admin.site.register(Link)
admin.site.register(Post)
admin.site.register(Person)
admin.site.register(By)


#admin.site.register(Arb, ArbAdmin)
#class ArbAdmin(admin.ModelAdmin):
#    list_display = ()
#    search_fields = ['title','subtitle','creators','body']
#admin.site.register(Item, ItemAdmin)
