from modeltranslation.translator import register, TranslationOptions
from .models import Marathon, FAQ, MarathonTarif


@register(Marathon)
class MarathonTranslationOptions(TranslationOptions):
    fields = ["name", "public_offer_link", "description"]
    required_languages = ["uz", "ru"]


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ["question", "answer"]
    required_languages = ["uz", "ru"]


@register(MarathonTarif)
class MarathonTarifTranslationOptions(TranslationOptions):
    fields = ["name", "description"]
    required_languages = ["uz", "ru"]
