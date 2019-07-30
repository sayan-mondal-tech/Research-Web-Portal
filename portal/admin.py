from django.contrib import admin
from .models import Application,Slot,Fee
# Register your models here.

admin.site.register(Application)
admin.site.register(Fee)
admin.site.register(Slot)

class ApplicationAdmin(admin.ModelAdmin):
	readonly_fields = ('application_no',)
	def get_readonly_fields(self, request, obj=None):
	    if obj is None:
	        return ['application_no']
	    return []
