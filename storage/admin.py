from django.contrib import admin
from storage.models import Part


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    pass
