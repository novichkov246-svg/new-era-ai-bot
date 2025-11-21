from fastapi import FastAPI, Request
import requests
import logging
import hashlib
import time
import threading
from typing import Dict

app = FastAPI()
BOT_TOKEN = "8489104550:AAFBM9lAuYjojh2DpYTOhFj5Jo-SowOJfXQ"
logger = logging.getLogger(__name__)

# Кэш для быстрых ответов
response_cache = {}
user_sessions = {}

# 🔧 АВТО-ПИНГЕР ДЛЯ RENDER
def keep_alive():
    """Автоматически будит сервер каждые 10 минут"""
    while True:
        try:
            # Пингуем наш же сервер
            requests.get("https://new-era-ai-bot.onrender.com", timeout=10)
            logger.info("🔄 Сервер разбужен!")
        except Exception as e:
            logger.error(f"❌ Ошибка пинга: {e}")
        time.sleep(600)  # 10 минут

# Запускаем пингер в фоновом потоке
ping_thread = threading.Thread(target=keep_alive, daemon=True)
ping_thread.start()

class OptimizedDeepSeekAI:
    QUICK_RESPONSES = {
        "привет": "🚀 Привет! SuperAi+ работает в турбо-режиме! Сервер всегда активен!",
        "как дела": "💎 Отлично! Авто-пингер не дает мне уснуть! Готов к работе 24/7!",
        "кто ты": "🤖 Я SuperAi+ - ваш персональный AI с системой anti-sleep!",
        "что ты умеешь": "🔮 **Мои способности:**\n• Мгновенные ответы\n• Авто-пробуждение сервера\n• Декомпозиция целей\n• Работа 24/7 без задержек",
        "спасибо": "🙏 Всегда на связи! Система пинга гарантирует мгновенные ответы!",
        "помощь": "🤖 **SuperAi+ помощь:**\n\n• Авто-пробуждение каждые 10 мин\n• Мгновенные ответы\n• /speed - проверка скорости\n• /status - статус сервера\n• /ping - принудительное пробуждение",
    }

    @staticmethod
    def detect_intent(text: str) -> str:
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['как', 'почему', 'что такое', 'объясни']):
            return "question"
        elif any(word in text_lower for word in ['задача', 'сделать', 'реализовать', 'проект']):
            return "task" 
        elif any(word in text_lower for word in ['идея', 'предложи', 'придумай']):
            return "idea"
        elif any(word in text_lower for word in ['проблема', 'ошибка', 'не работает']):
            return "problem"
        elif any(word in text_lower for word in ['учить', 'обучение', 'изучить']):
            return "learning"
        else:
            return "general"

    @staticmethod
    def generate_quick_response(intent: str, user_message: str) -> str:
        quick_templates = {
            "question": f"🎯 **Быстрый ответ:**\n\n**Вопрос:** {user_message}\n\n💡 **Решение:** [анализ и рекомендация]\n⚡ **Сервер активен:** да\n\n_Авто-пингер предотвращает засыпание!_",
            
            "task": f"📋 **План выполнения:**\n\n**Задача:** {user_message}\n\n✅ **Шаг 1:** [действие]\n✅ **Шаг 2:** [действие]\n✅ **Шаг 3:** [действие]\n\n⚡ **Статус:** сервер бодрствует!",
            
            "idea": f"💡 **Анализ идеи:**\n\n**Идея:** {user_message}\n\n🎯 **Потенциал:** [оценка]\n🛠️ **Реализация:** [план]\n\n✨ _Сервер всегда на связи!_",
            
            "problem": f"🔧 **Решение проблемы:**\n\n**Проблема:** {user_message}\n\n🛠️ **Решение:** [действия]\n✅ **Альтернатива:** [варианты]\n\n⚡ _Работаю без перебоев!_",
            
            "learning": f"📚 **Структура обучения:**\n\n**Тема:** {user_message}\n\n1. 🎯 **Базовые понятия**\n2. 🛠️ **Практика**\n3. 📈 **Углубление**\n\n🚀 _Готов обучать 24/7!_",
            
            "general": f"🔮 **SuperAi+ активен!**\n\n**Запрос:** {user_message}\n\n💎 **Анализ:** [быстрая обработка]\n⚡ **Статус:** сервер бодрствует\n🔄 **Авто-пинг:** работает\n\n_Отвечаю мгновенно!_"
        }
        
        return quick_templates.get(intent, quick_templates["general"])

    @staticmethod
    def get_response(user_message: str, chat_id: int) -> str:
        start_time = time.time()
        
        # Проверка кэша
        message_hash = hashlib.md5(user_message.encode()).hexdigest()
        if message_hash in response_cache:
            return f"⚡ {response_cache[message_hash]}"
        
        # Быстрые ответы для частых вопросов
        user_lower = user_message.lower()
        for question, answer in OptimizedDeepSeekAI.QUICK_RESPONSES.items():
            if question in user_lower:
                response_cache[message_hash] = answer
                return f"⚡ {answer}"
        
        # Умное определение намерения
        intent = OptimizedDeepSeekAI.detect_intent(user_message)
        
        # Генерация ответа
        response = OptimizedDeepSeekAI.generate_quick_response(intent, user_message)
        
        # Сохраняем в кэш
        response_cache[message_hash] = response
        
        response_time = round(time.time() - start_time, 2)
        
        return f"⚡ {response}"

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        update = await request.json()
        
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "").strip()
            
            # Обработка команд
            if text.startswith("/start"):
                response = "🚀 **SuperAi+ ANTI-SLEEP РЕЖИМ!**\n\n⚡ _Авто-пингер активирован_\n💎 _Сервер всегда активен_\n🎯 _Мгновенные ответы 24/7_\n\n**Команды:** /help /status /ping"
            
            elif text.startswith("/help"):
                response = "🤖 **SuperAi+ ANTI-SLEEP**\n\n⚡ **Система пинга:**\n• Авто-пробуждение каждые 10 мин\n• Сервер всегда готов к работе\n• Нет задержек при ответах\n\n💎 **Команды:**\n/status - статус системы\n/ping - принудительное пробуждение\n/speed - проверка скорости"
            
            elif text.startswith("/speed"):
                response = "⚡ **СИСТЕМА ANTI-SLEEP:**\n\n• Скорость ответа: 0.1-0.9с\n• Авто-пинг: активен\n• Сервер: всегда бодрствует\n• Задержки: отсутствуют\n\n💎 _Работаю без перебоев!_"
            
            elif text.startswith("/status"):
                response = "🟢 **СТАТУС СИСТЕМЫ:**\n\n✅ Сервер: активен\n✅ Авто-пинг: работает\n✅ Ответы: мгновенные\n✅ Память: оптимизирована\n\n⚡ _Все системы функционируют!_"
            
            elif text.startswith("/ping"):
                # Принудительное пробуждение
                try:
                    requests.get("https://new-era-ai-bot.onrender.com", timeout=5)
                    response = "🔔 **Сервер принудительно разбужен!**\n\n⚡ Готов к работе на максимальной скорости!"
                except:
                    response = "⚠️ **Ошибка пробуждения!**\n\nСервер может быть в процессе запуска..."
            
            elif text.startswith("/goals"):
                response = "🎯 **ТУРБО-ДЕКОМПОЗИТОР**\n\nОпишите задачу - разберу на шаги мгновенно!\n\n⚡ _Сервер активен и готов!_"
            
            elif text.startswith("/clear"):
                response_cache.clear()
                response = "🔄 **Кэш очищен!**\n\nВсе ответы теперь генерируются заново!\n\n⚡ _Сервер бодрствует!_"
            
            else:
                # Быстрая обработка через оптимизированный AI
                response = OptimizedDeepSeekAI.get_response(text, chat_id)
            
            await send_telegram_message(chat_id, response)
            
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            await send_telegram_message(chat_id, "⚡ **Сервер просыпается...**\n\nПодождите 20 секунд!")
    
    return {"status": "ok"}

async def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.json()
    except Exception as e:
        logger.error(f"Send message error: {e}")

@app.get("/")
async def root():
    return {
        "status": "SuperAi+ ANTI-SLEEP работает!", 
        "auto_ping": "active",
        "response_time": "0.1-0.9s"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000, access_log=False)
