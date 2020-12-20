from django.contrib import admin
from .models import Report


# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'TRIP_ID', 'device', 'driver', 'firm', 'vehicle', 'STARTEDT', 'STARTADDRESS', 'STARTODO', 'ENDEDT',
        'ENDADDRESS', 'ENDODO')


admin.site.register(Report, ReportAdmin)
