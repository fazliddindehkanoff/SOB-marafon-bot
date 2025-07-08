from django.db import models
from .constants import LANGUAGES, REGIONS


class Marathon(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateField()
    public_offer_link = models.CharField(max_length=250)
    description = models.TextField()


class MarathonTarif(models.Model):
    marathon = models.ForeignKey(
        Marathon, on_delete=models.CASCADE, related_name="tarifs"
    )
    private_channel_link = models.CharField(
        max_length=150, default="", blank=False, null=False
    )
    private_group_link = models.CharField(
        max_length=150, default="", null=True, blank=True
    )
    description = models.TextField(default="")
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Marathon Tarif"
        verbose_name_plural = "Marathon Tariflar"

    def __str__(self):
        return f"{self.name} - {self.marathon.name}"


class FAQ(models.Model):
    question = models.CharField(max_length=500, verbose_name="Savol")
    answer = models.TextField(verbose_name="Javob")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ["order"]


class BotAdminContactSettings(models.Model):
    admin_username = models.CharField(
        max_length=100,
        verbose_name="Admin Telegram username",
        help_text="@ belgisisiz",
    )


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(
        unique=True, null=True, blank=True, db_index=True
    )
    full_name = models.CharField(max_length=200, verbose_name="Ism Familiya")
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Telefon raqam",
    )
    region = models.CharField(
        max_length=20,
        choices=REGIONS,
        verbose_name="Viloyat",
    )
    language = models.CharField(
        max_length=2, choices=LANGUAGES, default="uz", verbose_name="Til"
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    is_subscribed = models.BooleanField(default=False, verbose_name="Obuna")
    chosen_tarif = models.ForeignKey(
        MarathonTarif,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Tanlangan Tarif",
    )

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.full_name}"
