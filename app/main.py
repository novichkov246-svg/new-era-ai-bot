from fastapi import FastAPI, Request
import requests
import logging
import json
import time
from typing import Dict

# Импорт наших сервисов
from app.services.stt_tts import voice_processor
from app.services.vision import vision_processor
from app.services.ai_client import ai_client
from app.core.subscriptions import subscription_manager, Tariff

app = FastAPI(title="SuperAi+ Pro", version="6.0")
BOT_TOKEN = "8489104550:AAFBM9lAuYjojh2DpYTOhFj5Jo-SowOJfXQ"
logger = logging.getLogger(__name__)

# 🔥 ВСПЛЫВАЮЩЕЕ МЕНЮ
MENU_KEYBOARD = {
    "keyboard": [
        ["🎤 Голосовой", "🖼️ Анализ фото"],
        ["🎯 Декомпозитор", "💎 Память"],
        ["🧠 Нейроны", "📊 Статистика"],
        ["💳 Тарифы", "ℹ️ Помощь"]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": False
}

class SuperAIPlus:
    def __init__(self):
        self.user_memory = {}
        self.user_neurons = {}
        
    def _ensure_user_data(self, user_id: int):
        if user_id not in self.user_memory:
            self.user_memory[user_id] = {"conversations": [], "goals": []}
        if user_id not in self.user_neurons:
            self.user_neurons[user_id] = 100
    
    def _check_limit(self, user_id: int, feature: str) -> bool:
        return subscription_manager.can_use_feature(user_id, feature)
    
    def _record_usage(self, user_id: int, feature: str):
        subscription_manager.record_usage(user_id, feature)
    
    def _get_limit_message(self, user_id: int) -> str:
        stats = subscription_manager.get_usage_stats(user_id)
        return f"""🔒 **Лимит исчерпан!**

📊 **Использовано сегодня:**
• AI-запросы: {stats['usage']['ai_requests']}
• Голосовые сообщения: {stats['usage']['voice_messages']}  
• Анализ изображений: {stats['usage']['image_analysis']}

💎 **Тариф:** {stats['tariff']}
💳 **Увеличьте лимиты:** /tariff"""
    
    def get_intelligent_response(self, message: str, user_id: int) -> str:
        self._ensure_user_data(user_id)
        message_lower = message.lower()
        
        # 🔒 ПРОВЕРКА ЛИМИТА
        if not self._check_limit(user_id, "ai_request"):
            return self._get_limit_message(user_id)
        self._record_usage(user_id, "ai_request")
        
        # 🧠 ОСНОВНЫЕ КОМАНДЫ
        if any(word in message_lower for word in ["привет", "старт"]):
            return "🚀 **SuperAi+ PRO АКТИВИРОВАН!**\n\n💎 _Система подписок активна_\n🎯 _Умные ограничения_\n⚡ _Полный функционал_\n\n👇 **Используйте меню:**"
        
        elif "помощь" in message_lower:
            return self._help_response()
        
        elif any(word in message_lower for word in ["тариф", "подписк", "оплат"]):
            return self._tariff_info(user_id)
        
        elif any(word in message_lower for word in ["статистик", "использован", "лимит"]):
            return self._usage_info(user_id)
        
        elif any(word in message_lower for word in ["голос", "аудио"]):
            return "🎤 **Голосовой режим:**\n\nОтправьте голосовое сообщение - распознаю и отвечу!\n\n🔒 _Лимит: зависит от тарифа_"
        
        elif any(word in message_lower for word in ["фото", "изображен"]):
            return "🖼️ **Анализ изображений:**\n\nОтправьте фото - проанализирую содержимое!\n\n🔒 _Лимит: зависит от тарифа_"
        
        elif any(word in message_lower for word in ["цел", "задач", "декомпоз"]):
            return "🎯 **Декомпозитор целей:**\n\nОпишите цель - разобью на шаги!\n\n💡 Пример: \"Выучить Python за 3 месяца\""
        
        elif any(word in message_lower for word in ["памят", "кристал"]):
            return f"💎 **Кристаллы памяти:**\n\nСохранено диалогов: {len(self.user_memory[user_id]['conversations'])}\nЦелей: {len(self.user_memory[user_id]['goals'])}"
        
        elif any(word in message_lower for word in ["нейрон", "баланс"]):
            return f"🧠 **Система Нейронов:**\n\nБаланс: {self.user_neurons[user_id]} нейронов\n\n💫 Зарабатывайте за активность!"
        
        # 🧠 УМНЫЕ ОТВЕТЫ
        else:
            self.user_neurons[user_id] += 1
            self.user_memory[user_id]["conversations"].append({
                "user": message, "timestamp": time.time()
            })
            
            responses = [
                f"🧠 **Анализирую запрос...**\n\n**{message}**\n\n💡 Используйте меню для выбора функций!",
                f"🔮 **По вашему вопросу:**\n\n{message}\n\n🎯 Готов помочь с решением!",
                f"💎 **Интересно!**\n\n{message}\n\n🚀 SuperAi+ к вашим услугам!"
            ]
            import random
            return random.choice(responses)
    
    async def handle_voice_message(self, voice_url: str, user_id: int) -> str:
        if not self._check_limit(user_id, "voice_message"):
            return self._get_limit_message(user_id)
        self._record_usage(user_id, "voice_message")
        
        try:
            text = await voice_processor.speech_to_text(voice_url)
            self.user_neurons[user_id] += 2
            
            if text:
                return f"🎤 **Распознано:**\n\n_{text}_\n\n💡 **Ответ:** Использую передовые STT технологии!"
            return "❌ Не удалось распознать голос. Попробуйте ещё раз!"
        except:
            return "🔧 Ошибка обработки голоса. Используйте текст."
    
    async def handle_image_message(self, image_url: str, user_id: int) -> str:
        if not self._check_limit(user_id, "image_analysis"):
            return self._get_limit_message(user_id)
        self._record_usage(user_id, "image_analysis")
        
        try:
            analysis = await vision_processor.analyze_image(image_url)
            self.user_neurons[user_id] += 3
            
            if analysis:
                return f"🖼️ **Анализ изображения:**\n\n📝 {analysis.get('description', 'Описание')}\n\n🔍 Использую компьютерное зрение!"
            return "❌ Не удалось проанализировать изображение."
        except:
            return "🔧 Ошибка анализа изображения."
    
    async def decompose_goal(self, goal: str, user_id: int) -> str:
        try:
            result = await ai_client.decompose_goal(goal)
            self.user_neurons[user_id] += 2
            
            if result:
                steps = "\n".join([f"{s['step']}. {s['action']}" for s in result["steps"]])
                return f"🎯 **Цель:** {goal}\n\n📋 **План:**\n{steps}\n\n💫 Цель сохранена!"
            return "❌ Не удалось разобрать цель."
        except:
            return "🔧 Ошибка декомпозитора."
    
    def _help_response(self) -> str:
        return """🤖 **SuperAi+ PRO - ПОМОЩЬ**

🎯 **ФУНКЦИИ:**
🎤 Голосовой - голосовые сообщения
🖼️ Анализ фото - работа с изображениями  
🎯 Декомпозитор - разбор целей на шаги
💎 Память - сохранение контекста
🧠 Нейроны - внутренняя валюта
📊 Статистика - использование и лимиты
💳 Тарифы - система подписок

⚡ **Выбирайте функции в меню!**"""
    
    def _tariff_info(self, user_id: int) -> str:
        current = subscription_manager.get_user_tariff(user_id)
        stats = subscription_manager.get_usage_stats(user_id)
        
        return f"""💳 **СИСТЕМА ПОДПИСОК**

🎯 **Ваш тариф:** {stats['tariff']}
📊 **Лимиты:**
• AI-запросы: {stats['usage']['ai_requests']}/день
• Голосовые: {stats['usage']['voice_messages']}/день  
• Изображения: {stats['usage']['image_analysis']}/день

💎 **Доступные тарифы:**
• Базовый (249₽) - 20 запросов/день
• Стандарт (890₽) - 100 запросов/день  
• PRO (2089₽) - 500 запросов/день
• PREMIUM (3989₽) - 1000 запросов/день

🚀 **Для улучшения:** /upgrade"""
    
    def _usage_info(self, user_id: int) -> str:
        stats = subscription_manager.get_usage_stats(user_id)
        return f"""📊 **СТАТИСТИКА ИСПОЛЬЗОВАНИЯ**

💎 **Тариф:** {stats['tariff']}
🧠 **Нейроны:** {self.user_neurons.get(user_id, 100)}

📈 **Использовано сегодня:**
• AI-запросы: {stats['usage']['ai_requests']}
• Голосовые сообщения: {stats['usage']['voice_messages']}
• Анализ изображений: {stats['usage']['image_analysis']}

💾 **Память:**
• Диалогов: {len(self.user_memory.get(user_id, {}).get('conversations', []))}
• Целей: {len(self.user_memory.get(user_id, {}).get('goals', []))}"""

ai_engine = SuperAIPlus()

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        update = await request.json()
        
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            user_id = update["message"]["from"]["id"]
            
            # 🎤 ГОЛОСОВЫЕ СООБЩЕНИЯ
            if "voice" in update["message"]:
                response = await ai_engine.handle_voice_message("voice_url", user_id)
                await send_message(chat_id, response, menu=True)
            
            # 🖼️ ИЗОБРАЖЕНИЯ
            elif "photo" in update["message"]:
                response = await ai_engine.handle_image_message("image_url", user_id)
                await send_message(chat_id, response, menu=True)
            
            # 💬 ТЕКСТ
            elif "text" in update["message"]:
                text = update["message"]["text"].strip()
                
                if text.startswith("/start"):
                    response = "🚀 **SuperAi+ PRO!**\n\n💎 Полный функционал\n🔒 Умные ограничения\n⚡ Работает 24/7\n\n👇 Используйте меню:"
                    await send_message(chat_id, response, menu=True)
                
                elif text.startswith("/help"):
                    response = ai_engine._help_response()
                    await send_message(chat_id, response, menu=True)
                
                elif text.startswith("/tariff") or text.startswith("/upgrade"):
                    response = ai_engine._tariff_info(user_id)
                    await send_message(chat_id, response, menu=True)
                
                elif text.startswith("/usage") or text.startswith("/stats"):
                    response = ai_engine._usage_info(user_id)
                    await send_message(chat_id, response, menu=True)
                
                elif text.startswith("/decompose"):
                    goal = text.replace("/decompose", "").strip()
                    if goal:
                        response = await ai_engine.decompose_goal(goal, user_id)
                    else:
                        response = "🎯 Напишите цель: /decompose Ваша цель"
                    await send_message(chat_id, response, menu=True)
                
                else:
                    response = ai_engine.get_intelligent_response(text, user_id)
                    await send_message(chat_id, response, menu=True)
                
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    
    return {"status": "ok"}

async def send_message(chat_id: int, text: str, menu: bool = False):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    if menu:
        payload["reply_markup"] = json.dumps(MENU_KEYBOARD)
    
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

@app.get("/")
async def root():
    return {"status": "SuperAi+ PRO с подписками работает!"}

# 🔧 АВТО-ПИНГЕР
import threading
def keep_alive():
    while True:
        try:
            requests.get("https://new-era-ai-bot.onrender.com", timeout=5)
        except:
            pass
        time.sleep(300)

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
