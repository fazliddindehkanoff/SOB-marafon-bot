from django.contrib import admin
from django.urls import path
from bot.views import telegram_webhook
from core.admin import custom_admin_index

admin.site.index = custom_admin_index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("webhook/", telegram_webhook),
]
