from django.contrib import admin
from cash.models import *


class TransferAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'source', 'destination', 'validity_date')
    list_filter = ('validity_date', 'source', 'destination')
    ordering = ('-validity_date',)
    search_fields = ('description',)
    date_hierarchy = 'validity_date'

class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transfer, TransferAdmin)
admin.site.register(Account, AccountAdmin)

