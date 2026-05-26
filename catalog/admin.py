from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import AlcoholType, Taster, Beverage, Snack, Flavor


@admin.register(Taster)
class TasterAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("experience_level",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional information from the sommelier",
            {"fields": ("experience_level", "preferred_flavors")},
        ),
    )
    filter_horizontal = ("preferred_flavors",)


@admin.register(Beverage)
class BeverageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "alcohol_type",
        "alcohol_strength",
        "average_price",
    )
    search_fields = ("name", "description")
    list_filter = ("alcohol_type", "flavors")
    filter_horizontal = ("flavors", "snacks", "tasters")


@admin.register(AlcoholType)
class AlcoholTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Snack)
class SnackAdmin(admin.ModelAdmin):
    list_display = ("name", "is_cooking_required")
    list_filter = ("is_cooking_required",)


@admin.register(Flavor)
class FlavorAdmin(admin.ModelAdmin):
    list_display = ("name",)
