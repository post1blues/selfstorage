from django.contrib import admin

from .models import Storage, Box, Payment, SeasonService, SeasonOrder, StorageOrder


admin.site.register(Storage)
admin.site.register(Box)
admin.site.register(Payment)
admin.site.register(SeasonService)
admin.site.register(SeasonOrder)
admin.site.register(StorageOrder)