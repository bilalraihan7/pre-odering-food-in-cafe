from django.contrib import admin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

from . models import *

admin.site.register(User)
admin.site.register(booking)
admin.site.register(vehicle)
admin.site.register(Payment)
class DriversAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'status', 'is_verified', 'view_license_button')
    list_filter = ('status', 'is_verified')
    search_fields = ('name','phone',)

    def view_license_button(self, obj):
        url = reverse('view_license', args=[obj.pk])
        return format_html('<a class="button" href="{}">View License</a>', url)

    view_license_button.short_description = ''

    def verify_license(self, request, queryset):
        for provider in queryset:
            provider.status = 'Verified'
            provider.is_verified = True
            provider.save()

    verify_license.short_description = "Verify selected providers' licenses"

    actions = [verify_license]

admin.site.register(Driver,DriversAdmin)