from django.contrib import admin

from physicalbook.models import PhysicalBook


@admin.register(PhysicalBook)
class PhysicalBookAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
