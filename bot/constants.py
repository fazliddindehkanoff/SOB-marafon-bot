from enum import Enum

REGIONS = [
    ("tashkent", "Toshkent"),
    ("samarkand", "Samarqand"),
    ("bukhara", "Buxoro"),
    ("andijan", "Andijon"),
    ("fergana", "Farg'ona"),
    ("namangan", "Namangan"),
    ("kashkadarya", "Qashqadaryo"),
    ("surkhandarya", "Surxondaryo"),
    ("khorezm", "Xorazm"),
    ("navoi", "Navoiy"),
    ("jizzakh", "Jizzax"),
    ("sirdarya", "Sirdaryo"),
    ("karakalpakstan", "Qoraqalpog'iston"),
]

LANGUAGES = [
    ("uz", "O'zbek"),
    ("ru", "Русский"),
]


class Buttons(Enum):
    uzbek_lang = "🇺🇿 O'zbekcha"
    russian_lang = "🇷🇺 Русский"
    send_phone_number = {
        "uz": "📲 Telefon raqamini yuborish",
        "ru": "📲 Отправить номер телефона",
    }
    faq = {
        "uz": "❓ Ko'p beriladigan savollar",
        "ru": "❓ Часто задаваемые вопросы",
    }
    back = {
        "uz": "🔙 Orqaga",
        "ru": "🔙 Назад",
    }
    settings = {
        "uz": "⚙️ Sozlamalar",
        "ru": "⚙️ Настройки",
    }
    tariffs = {
        "uz": "💰 Tariflar",
        "ru": "💰 Тарифы",
    }
    contact = {
        "uz": "📞 Biz bilan bog'lanish",
        "ru": "📞 Связаться с нами",
    }
    change_language = {
        "uz": "🌐 Tilni o'zgartirish",
        "ru": "🌐 Изменить язык",
    }
    change_phone = {
        "uz": "📲 Telefon raqamini o'zgartirish",
        "ru": "📲 Изменить номер телефона",
    }
    change_region = {
        "uz": "📍 Viloyatni o'zgartirish",
        "ru": "📍 Изменить регион",
    }
    join_group = {
        "uz": "👥 Guruhga qo'shilish",
        "ru": "👥 Присоединиться к группе",
    }
    join_channel = {
        "uz": "📢 Kanalga qo'shilish",
        "ru": "📢 Присоединиться к каналу",
    }


class Messages(Enum):
    greeting_uz = "🇺🇿 Salom!\nKeling, avvaliga xizmat ko‘rsatish tilini tanlab olaylik!"
    greeting_ru = "🇷🇺 Здравствуйте!\nДавайте для начала выберем язык обслуживания!"
    send_phone_number = {
        "uz": "👇 Pastdagi tugma orqali telefon raqamingizni yuboring yoki 📞 raqamingizni +998901234567 formatida kiriting:",
        "ru": "👇 Отправьте свой номер телефона, используя кнопку ниже, или введите свой 📞 номер в формате +998901234567:",
    }
    send_name = {"uz": "👤 Ismingizni kiriting:", "ru": "👤 Введите своё имя:"}
    main_menu = {
        "uz": "📋 Asosiy menyu",
        "ru": "📋 Главное меню",
    }
    min_quantity = {
        "uz": "❗️ Mahsulotning minimal miqdori: 1",
        "ru": "❗️ Минимальное количество товара: 1",
    }
    choose_region = {
        "uz": "📍 Iltimos, mintaqani tanlang:",
        "ru": "📍 Пожалуйста, выберите регион:",
    }
    terms = {"uz": "Public terms in uz {}", "ru": "Public terms in ru {}"}
    settings = {"uz": "⚙️ Sozlamalar:", "ru": "⚙️ Настройки:"}
    language_changed = {
        "uz": "Til muvaffaqiyatli o'zgartirildi",
        "ru": "Язык успешно изменен",
    }
    phone_changed = {
        "uz": "Telefon raqami muvaffaqiyatli o'zgartirildi",
        "ru": "Номер телефона успешно изменен",
    }
    region_changed = {
        "uz": "Viloyat muvaffaqiyatli o'zgartirildi",
        "ru": "Регион успешно изменен",
    }
    payment_successful = {
        "uz": "✅ To'lov muvaffaqiyatli bajarildi!\n\nGuruhga qo'shilish uchun quyidagi tugmani bosing",
        "ru": "✅ Платеж успешно выполнен!\n\nНажмите на кнопку ниже, чтобы присоединиться к группе",
    }
    region_title = {
        "uz": "📍 Manzilingizni yozishingiz mumkin",
        "ru": "📍 Вы можете написать свой адрес",
    }
