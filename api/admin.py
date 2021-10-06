from django.contrib import admin
from .models import (
    NewUser,
    Artist,
    ArtistFollow,
    Request,
    Problem,
    Venue,
    Ticket,
    Promoter,
    Event,
    EventFollow,
    AmazonKey,
)
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = (
        "user_name",
        "name",
    )
    list_filter = ("user_name", "name", "is_active", "is_staff")
    ordering = ("-start_date",)
    list_display = ("id", "user_name", "name", "is_active", "is_staff")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_name",
                    "name",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user_name",
                    "name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Artist)
admin.site.register(ArtistFollow)
admin.site.register(Request)
admin.site.register(Problem)
admin.site.register(Venue)
admin.site.register(Ticket)
admin.site.register(Promoter)
admin.site.register(Event)
admin.site.register(EventFollow)
admin.site.register(AmazonKey)
