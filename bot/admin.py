from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from django.contrib.auth.models import User, Group
from modeltranslation.admin import TabbedTranslationAdmin

from .models import (
    TelegramUser,
    Marathon,
    FAQ,
    BotAdminContactSettings,
    MarathonTarif,
)

admin.site.unregister(User)
admin.site.unregister(Group)


class MarathonTarifAdmin(TabularInline):
    model = MarathonTarif
    fields = [
        "name_uz",
        "name_ru",
        "price",
        "private_channel_link",
        "private_group_link",
        "description_uz",
        "description_ru",
    ]
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        form = formset.form

        form.base_fields["name_uz"].label = "Name (Uz)"
        form.base_fields["name_ru"].label = "Name (Ru)"
        form.base_fields["description_uz"].label = "Description (Uz)"
        form.base_fields["description_ru"].label = "Description (Ru)"
        form.base_fields["private_channel_link"].label = "Private Channel Link *"
        return formset


@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_filter = ["is_subscribed", "chosen_tarif"]
    list_display = [
        "full_name",
        "phone_number",
        "language",
        "is_subscribed",
        "chosen_tarif",
    ]


@admin.register(FAQ)
class FAQAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "question_uz", "question_ru"]


@admin.register(Marathon)
class MarathonAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "name_uz", "name_ru"]
    inlines = [MarathonTarifAdmin]


@admin.register(BotAdminContactSettings)
class BotAdminContactSettingsAdmin(ModelAdmin):
    def has_add_permission(self, request):
        # Allow add only if there are no existing objects
        if BotAdminContactSettings.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    list_display = ["id", "admin_username"]
