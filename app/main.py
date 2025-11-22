from fastapi import FastAPI, Request
import requests
import logging
import json
import time
import os
import random
import math
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SuperAi+ Pro", version="7.0")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8489104550:AAFBM9lAuYjojh2DpYTOhFj5Jo-SowOJfXQ")

MENU_KEYBOARD = {
    "keyboard": [
        ["🎤 Голосовой", "🖼️ Анализ фото"],
        ["🎯 Декомпозитор", "💎 Память"],
        ["🧠 Нейроны", "📊 Статистика"],
        ["💳 Тарифы", "ℹ️ Помощь"]
    ],
    "resize_keyboard": True
}

class SuperAIPlus:
    def __init__(self):
        self.user_data = {}
    
    def _ensure_user(self, user_id):
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                'neurons': 100,
                'crystals': 50,
                'conversations': [],
                'usage': {'ai': 0, 'voice': 0, 'image': 0, 'goals': 0}
            }
    
    def get_smart_response(self, message: str, user_id: int) -> str:
        self._ensure_user(user_id)
        message_lower = message.lower().strip()
        
        # 🎯 ОБРАБОТКА КНОПОК МЕНЮ
        if message == "🎤 Голосовой":
            return "🎤 **Голосовой режим:**\n\nОтправьте голосовое сообщение - я его распознаю!"
        
        elif message == "🖼️ Анализ фото":
            return "🖼️ **Анализ изображений:**\n\nОтправьте фото - я проанализирую его содержимое!"
        
        elif message == "🎯 Декомпозитор":
            return "🎯 **Декомпозитор целей:**\n\nИспользуйте команду: /decompose Ваша цель\n\nНапример: /decompose Научиться программировать"
        
        elif message == "💎 Память":
            user = self.user_data[user_id]
            return f"💎 **Память:**\n\nКристаллы: {user['crystals']}\nДиалогов: {len(user['conversations'])}"
        
        elif message == "🧠 Нейроны":
            user = self.user_data[user_id]
            return f"🧠 **Нейроны:**\n\nБаланс: {user['neurons']}\n\n+1 за каждый вопрос!\n+2 за голосовые\n+3 за анализ фото"
        
        elif message == "📊 Статистика":
            return self.get_stats(user_id)
        
        elif message == "💳 Тарифы":
            return """💳 **Тарифы:**

🆓 Базовый: 249₽/мес
• 100 AI-запросов/день
• 20 голосовых/день  
• 10 анализов фото/день

🚀 PRO: 899₽/мес
• 500 AI-запросов/день
• 100 голосовых/день
• 50 анализов фото/день

💎 Premium: 1899₽/мес
• Безлимитные запросы
• Приоритетная поддержка"""
        
        elif message == "ℹ️ Помощь":
            return """🤖 **SuperAi+ PRO - Помощь**

🎯 **Функции:**
• 🎤 Голосовые сообщения
• 🖼️ Анализ изображений  
• 🎯 Декомпозитор целей
• 💎 Кристаллы памяти
• 🧠 Система нейронов
• 📊 Статистика
• 💳 Тарифы

💡 **Просто нажимайте кнопки меню или задавайте вопросы!**"""

        # 🔢 МАТЕМАТИКА
        if "корень из" in message_lower:
            try:
                number = float(message_lower.split("корень из")[1].strip())
                result = math.sqrt(number)
                self.user_data[user_id]['neurons'] += 2
                self.user_data[user_id]['usage']['ai'] += 1
                return f"🔢 Квадратный корень из {number} = {result:.4f}"
            except:
                return "🤔 Не могу вычислить корень. Пример: 'корень из 16'"
        
        # 🧮 ВЫЧИСЛЕНИЯ
        elif any(op in message_lower for op in ["+", "-", "*", "/"]):
            try:
                if "+" in message_lower:
                    parts = message_lower.split("+")
                    a, b = float(parts[0]), float(parts[1])
                    result = a + b
                elif "-" in message_lower:
                    parts = message_lower.split("-")
                    a, b = float(parts[0]), float(parts[1])
                    result = a - b
                elif "*" in message_lower:
                    parts = message_lower.split("*")
                    a, b = float(parts[0]), float(parts[1])
                    result = a * b
                elif "/" in message_lower:
                    parts = message_lower.split("/")
                    a, b = float(parts[0]), float(parts[1])
                    if b == 0:
                        return "❌ На ноль делить нельзя!"
                    result = a / b
                
                self.user_data[user_id]['neurons'] += 1
                self.user_data[user_id]['usage']['ai'] += 1
                return f"🧮 Результат: {result}"
            except:
                return "🤔 Не могу вычислить. Формат: '5 + 3'"
        
        # 💬 ОБЩИЕ ВОПРОСЫ
        responses = {
            "привет": "🚀 Привет! Я SuperAi+ - твой умный помощник! Используй меню для доступа ко всем функциям!",
            "как дела": "💫 Отлично! Работаю над интересными задачами. А у тебя?",
            "что ты умеешь": "🎯 Я умею: голосовые сообщения, анализ фото, декомпозицию целей, умные беседы и многое другое! Используй меню!",
            "спасибо": "😊 Всегда рад помочь!",
            "пока": "👋 До встречи!",
            "кто ты": "🤖 Я SuperAi+ - твой AI помощник!",
            "время": f"🕐 Сейчас {time.strftime('%H:%M:%S')}",
            "дата": f"📅 Сегодня {time.strftime('%d.%m.%Y')}",
        }
        
        for key, answer in responses.items():
            if key in message_lower:
                self.user_data[user_id]['neurons'] += 1
                self.user_data[user_id]['usage']['ai'] += 1
                return answer
        
        # 🔮 УМНЫЙ ОБЩИЙ ОТВЕТ
        self.user_data[user_id]['neurons'] += 1
        self.user_data[user_id]['usage']['ai'] += 1
        self.user_data[user_id]['conversations'].append(message)
        
        smart_responses = [
            f"💭 {message} - интересная тема! Что именно вас интересует?",
            f"🎯 По поводу {message} - давайте обсудим подробнее!",
            f"💡 {message} - хороший вопрос! Расскажите больше?",
        ]
        
        return random.choice(smart_responses)
    
    async def handle_voice_message(self, file_id: str, user_id: int) -> str:
        self._ensure_user(user_id)
        self.user_data[user_id]['usage']['voice'] += 1
        self.user_data[user_id]['neurons'] += 2
        
        # Имитация распознавания голоса
        voice_texts = [
            "Привет! Это тестовое распознавание голосового сообщения.",
            "Голосовое сообщение успешно обработано.",
            "Аудио распознано: пользователь отправил голосовое сообщение.",
        ]
        
        recognized_text = random.choice(voice_texts)
        self.user_data[user_id]['conversations'].append(f"🎤 {recognized_text}")
        
        return f"🎤 **Голосовое сообщение:**\n\n{recognized_text}"
    
    async def handle_image_message(self, file_id: str, user_id: int) -> str:
        self._ensure_user(user_id)
        self.user_data[user_id]['usage']['image'] += 1
        self.user_data[user_id]['neurons'] += 3
        
        # Имитация анализа изображения
        analyses = [
            "🖼️ **Анализ изображения:** На фото виден современный интерьер с хорошим освещением.",
            "🖼️ **Анализ изображения:** Фото показывает городской пейзаж с архитектурными элементами.",
            "🖼️ **Анализ изображения:** На изображении присутствуют люди в естественной обстановке.",
        ]
        
        analysis = random.choice(analyses)
        self.user_data[user_id]['conversations'].append(analysis)
        
        return analysis
    
    async def decompose_goal(self, goal: str, user_id: int) -> str:
        self._ensure_user(user_id)
        
        if not goal:
            return "🎯 Напишите цель после команды: /decompose Ваша цель"
        
        self.user_data[user_id]['usage']['goals'] += 1
        self.user_data[user_id]['neurons'] += 2
        self.user_data[user_id]['crystals'] += 5
        
        steps = [
            "Чётко сформулировать конечную цель",
            "Проанализировать текущую ситуацию",
            "Определить ключевые этапы",
            "Составить план с сроками",
            "Начать выполнение первого этапа"
        ]
        
        steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        
        return f"🎯 **Цель:** {goal}\n\n📋 **План:**\n\n{steps_text}\n\n💎 +5 кристаллов!"
    
    def get_stats(self, user_id: int) -> str:
        self._ensure_user(user_id)
        user = self.user_data[user_id]
        
        return f"""📊 **СТАТИСТИКА**

🧠 Нейроны: {user['neurons']}
💎 Кристаллы: {user['crystals']}
💾 Диалогов: {len(user['conversations'])}

📈 **Использование:**
• AI-запросы: {user['usage']['ai']}
• Голосовые: {user['usage']['voice']}
• Фото: {user['usage']['image']}
• Цели: {user['usage']['goals']}"""

ai_engine = SuperAIPlus()

async def get_telegram_file_url(file_id: str) -> str:
    try:
        file_info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        response = requests.get(file_info_url, timeout=10)
        
        if response.status_code == 200:
            file_info = response.json()
            if file_info.get("ok"):
                file_path = file_info["result"]["file_path"]
                return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        return ""
    except Exception as e:
        logger.error(f"Error getting file URL: {e}")
        return ""

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
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code != 200:
            logger.error(f"Failed to send message: {response.text}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        update = await request.json()
        
        import asyncio
        asyncio.create_task(process_update(update))
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "ok"}

async def process_update(update: dict):
    try:
        if "message" not in update:
            return
            
        chat_id = update["message"]["chat"]["id"]
        user_id = update["message"]["from"]["id"]
        
        if "voice" in update["message"]:
            file_id = update["message"]["voice"]["file_id"]
            response = await ai_engine.handle_voice_message(file_id, user_id)
            await send_message(chat_id, response, menu=True)
        
        elif "photo" in update["message"]:
            photo_sizes = update["message"]["photo"]
            file_id = photo_sizes[-1]["file_id"]
            response = await ai_engine.handle_image_message(file_id, user_id)
            await send_message(chat_id, response, menu=True)
        
        elif "text" in update["message"]:
            text = update["message"]["text"].strip()
            
            if text.startswith("/start"):
                response = "🚀 **SuperAi+ PRO!**\n\n💎 Все функции активны!\n\n👇 Используйте меню или просто общайтесь!"
                await send_message(chat_id, response, menu=True)
            elif text.startswith("/help"):
                response = ai_engine.get_smart_response("ℹ️ Помощь", user_id)
                await send_message(chat_id, response, menu=True)
            elif text.startswith("/stats"):
                response = ai_engine.get_stats(user_id)
                await send_message(chat_id, response, menu=True)
            elif text.startswith("/decompose"):
                goal = text.replace("/decompose", "").strip()
                response = await ai_engine.decompose_goal(goal, user_id)
                await send_message(chat_id, response, menu=True)
            else:
                response = ai_engine.get_smart_response(text, user_id)
                await send_message(chat_id, response, menu=True)
            
    except Exception as e:
        logger.error(f"Error processing update: {e}")

@app.get("/")
async def root():
    return {"status": "SuperAi+ PRO работает!", "version": "7.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
