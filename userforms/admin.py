from django.contrib import admin
from .models import *
from django.utils.html import format_html


# admin.site.register(Owner)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_id', 'make', 'color')


class DriverAdmin(admin.ModelAdmin):
    def myphoto(self, obj):
        return format_html('<img src="{}" width="50" />'.format(obj.photo.url))

    list_display = ('id', 'owner', 'first_name', 'myphoto')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'owner')


admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Device, DeviceAdmin)
