from django.contrib import admin

from .models import Ticket, TGAdmin, TGUser

admin.site.register(Ticket)
admin.site.register(TGAdmin)
admin.site.register(TGUser)
