import os
from dotenv import load_dotenv

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from aiogram import Bot, Dispatcher
from aiogram.types import Update

from bot.handlers import router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


@csrf_exempt
async def telegram_webhook(request):
    if request.method == "POST":
        try:
            update = Update.model_validate_json(request.body)
        except Exception as e:
            return HttpResponseBadRequest(f"Invalid update: {e}")

        # Process update directly as a coroutine
        await dp._process_update(bot, update)

        return JsonResponse({"ok": True})
    return HttpResponseBadRequest("Only POST method allowed")
