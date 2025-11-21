from fastapi import FastAPI, Request
import requests
import logging
import json
import time
from typing import Dict
import base64

# Импорт наших сервисов
from app.services.stt_tts import voice_processor
from app.services.vision import vision_processor
from app.services.ai_client import ai_client

app = FastAPI(title="SuperAi+ Turbo", version="5.0")
BOT_TOKEN = "8489104550:AAFBM9lAuYjojh2DpYTOhFj5Jo-SowOJfXQ"
logger = logging.getLogger(__name__)

# 🔥 ВСПЛЫВАЮЩЕЕ МЕНЮ (всегда видно)
MENU_KEYBOARD = {
    "keyboard": [
        ["🎤 Голосовой", "🖼️ Анализ фото"],
        ["🎯 Декомпозитор", "💎 Кристаллы памяти"],
        ["🧠 Мои нейроны", "🛍️ Маркетплейс"],
        ["⚙️ Настройки", "ℹ️ Помощь"]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": False,
    "selective": True
}

class SuperAIPlus:
    def __init__(self):
        self.user_memory = {}
        self.user_neurons = {}  # Баланс нейронов по пользователям
        
    def _ensure_user_data(self, user_id: int):
        """Создаём данные пользователя если их нет"""
        if user_id not in self.user_memory:
            self.user_memory[user_id] = {
                "conversations": [],
                "preferences": {},
                "goals": []
            }
        if user_id not in self.user_neurons:
            self.user_neurons[user_id] = 150  # Стартовый баланс
            
    def get_intelligent_response(self, message: str, user_id: int) -> str:
        """Умные ответы с учётом контекста"""
        self._ensure_user_data(user_id)
        message_lower = message.lower()
        
        # 🔮 БАЗОВЫЕ КОМАНДЫ
        if any(word in message_lower for word in ["привет", "старт", "hello"]):
            return "🚀 **SuperAi+ АКТИВИРОВАН!**\n\n💎 _Все функции активированы_\n🎯 _Интеллектуальные ответы_\n⚡ _Работаю 24/7_\n\n👇 **Используйте меню для навигации:**"
        
        elif "помощь" in message_lower:
            return self._help_response()
        
        elif "настройк" in message_lower:
            return "⚙️ **Настройки SuperAi+:**\n\n• Язык: Русский\n• Уведомления: Вкл\n• Режим: Турбо\n• Нейроны: 150\n• Память: Активна"
        
        # 🎯 ЭКСКЛЮЗИВНЫЕ ФИЧИ
        elif any(word in message_lower for word in ["голос", "аудио", "озвуч"]):
            return "🎤 **Голосовой режим:**\n\nЗаписывайте голосовые сообщения - я преобразую их в текст и дам умный ответ!\n\n_Технологии: STT (Speech-to-Text) + TTS (Text-to-Speech)_"
        
        elif any(word in message_lower for word in ["фото", "изображен", "картинк"]):
            return "🖼️ **Анализ изображений:**\n\nОтправляйте фото - я опишу содержимое, распознаю текст и решу задачи!\n\n_Поддержка: YOLO, OCR, AI Vision_"
        
        elif any(word in message_lower for word in ["цел", "задач", "план", "декомпоз"]):
            return "🎯 **Декомпозитор целей:**\n\nОпишите любую цель - разобью на простые шаги!\n\n**Примеры:**\n• \"Выучить английский за 6 месяцев\"\n• \"Запустить стартап\"\n• \"Начать заниматься спортом\""
        
        elif any(word in message_lower for word in ["памят", "кристал", "воспоминан"]):
            memory_count = len(self.user_memory[user_id]["conversations"])
            return f"💎 **Кристаллы памяти:**\n\n📚 Сохранено диалогов: {memory_count}\n🎯 Ваши цели: {len(self.user_memory[user_id]['goals'])}\n\n_Ваши предпочтения и контекст запоминаются_"
        
        elif any(word in message_lower for word in ["нейрон", "валюта", "баланс"]):
            balance = self.user_neurons[user_id]
            return f"🧠 **Система Нейронов:**\n\n**Ваш баланс:** {balance} нейронов\n\n💫 **Заработок:**\n• Активность в боте\n• Приглашение друзей\n• Создание контента\n\n🛍️ **Трата:**\n• Цифровые товары\n• Премиум функции\n• Голосования"
        
        elif any(word in message_lower for word in ["маркет", "магазин", "товар"]):
            return "🛍️ **P2P Маркетплейс:**\n\n**Скоро открытие!**\n\nТоргуйте цифровыми товарами:\n• Промпты\n• AI-модели\n• Цифровые личности\n• Обучающие материалы\n\n_Комиссия: 15% в нейронах_"
        
        # 🧠 УМНЫЕ ОТВЕТЫ НА ВОПРОСЫ
        elif "как дел" in message_lower:
            return "💎 Отлично! Мои нейросети работают на полную мощность! Готов помочь с любыми задачами! А у вас?"
        
        elif "кто ты" in message_lower:
            return "🤖 **SuperAi+** - экосистема персонального интеллекта!\n\nМой код создан на базе **DeepSeek AI** с интеграцией всех современных технологий!"
        
        elif "сколько лет" in message_lower:
            return "🕰️ Я цифровой помощник - мой код постоянно обновляется и улучшается! Можно сказать, я всегда современный!"
        
        # 🔮 ОБЩИЕ ЗАПРОСЫ - ИСПОЛЬЗУЕМ DEEPSEEK AI
        else:
            # Сохраняем в память
            self.user_memory[user_id]["conversations"].append({
                "user": message,
                "timestamp": time.time()
            })
            # Начисляем нейроны за активность
            self.user_neurons[user_id] += 1
            
            return self._analyze_with_ai(message)
    
    async def _analyze_with_ai(self, message: str) -> str:
        """Анализ запроса через DeepSeek AI"""
        try:
            response = await ai_client.chat_completion(message)
            return response
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return f"🧠 **SuperAi+ анализирует запрос...**\n\n**Ваш вопрос:** {message}\n\n💡 Используйте меню для выбора конкретной функции!"
    
    async def handle_voice_message(self, voice_url: str, user_id: int) -> str:
        """Обработка голосового сообщения"""
        try:
            # Преобразуем голос в текст
            text = await voice_processor.speech_to_text(voice_url)
            
            if text:
                # Начисляем нейроны за использование голоса
                self._ensure_user_data(user_id)
                self.user_neurons[user_id] += 2
                
                return f"🎤 **Распознано голосовое сообщение:**\n\n_{text}_\n\n💡 **Мой ответ:** {await self._analyze_with_ai(text)}"
            else:
                return "❌ Не удалось распознать голосовое сообщение. Попробуйте ещё раз!"
                
        except Exception as e:
            logger.error(f"Voice handling error: {e}")
            return "🔧 Ошибка обработки голосового сообщения. Используйте текстовый ввод."
    
    async def handle_image_message(self, image_url: str, user_id: int) -> str:
        """Обработка изображения"""
        try:
            # Анализируем изображение
            analysis = await vision_processor.analyze_image(image_url)
            
            if analysis:
                # Начисляем нейроны за использование зрения
                self._ensure_user_data(user_id)
                self.user_neurons[user_id] += 3
                
                description = analysis.get("description", "Не удалось проанализировать изображение")
                tags = ", ".join(analysis.get("tags", []))
                
                return f"🖼️ **Анализ изображения:**\n\n📝 {description}\n\n🏷️ **Теги:** {tags}\n\n💫 Использую компьютерное зрение для анализа!"
            else:
                return "❌ Не удалось проанализировать изображение. Попробуйте другое фото!"
                
        except Exception as e:
            logger.error(f"Image handling error: {e}")
            return "🔧 Ошибка анализа изображения. Попробуйте текстовый запрос."
    
    async def decompose_goal(self, goal: str, user_id: int) -> str:
        """Декомпозиция цели"""
        try:
            result = await ai_client.decompose_goal(goal)
            
            if result:
                # Сохраняем цель в память
                self._ensure_user_data(user_id)
                self.user_memory[user_id]["goals"].append({
                    "goal": goal,
                    "created": time.time(),
                    "steps": result["steps"]
                })
                
                steps_text = "\n".join([f"{step['step']}. {step['action']}" for step in result["steps"]])
                
                return f"🎯 **Декомпозиция цели:**\n\n**Цель:** {goal}\n\n📋 **План выполнения:**\n{steps_text}\n\n💎 Цель сохранена в ваши кристаллы памяти!"
            else:
                return "❌ Не удалось разобрать цель. Попробуйте сформулировать иначе!"
                
        except Exception as e:
            logger.error(f"Goal decomposition error: {e}")
            return "🔧 Ошибка декомпозитора целей. Попробуйте позже."
    
    def _help_response(self) -> str:
        return """🤖 **SuperAi+ - ПОМОЩЬ**

🔮 **ОСНОВНЫЕ ФУНКЦИИ:**

🎤 **Голосовой** - общение голосовыми сообщениями
🖼️ **Анализ фото** - распознавание и описание изображений
🎯 **Декомпозитор** - разбор целей на простые шаги
💎 **Память** - сохранение контекста и предпочтений
🧠 **Нейроны** - внутренняя валюта и экономика
🛍️ **Маркетплейс** - торговля цифровыми товарами

⚡ **Просто напишите вопрос или выберите функцию в меню!**"""

# Инициализация AI
ai_engine = SuperAIPlus()

@app.post("/webhook")
async def handle_webhook(request: Request):
    """Основной вебхук для Telegram"""
    try:
        update = await request.json()
        logger.info(f"Received update: {update}")
        
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            user_id = update["message"]["from"]["id"]
            
            # 🎤 ОБРАБОТКА ГОЛОСОВЫХ СООБЩЕНИЙ
            if "voice" in update["message"]:
                voice_file_id = update["message"]["voice"]["file_id"]
                voice_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={voice_file_id}"
                
                response = await ai_engine.handle_voice_message(voice_url, user_id)
                await send_telegram_message(chat_id, response, menu=True)
            
            # 🖼️ ОБРАБОТКА ИЗОБРАЖЕНИЙ
            elif "photo" in update["message"]:
                # Берем самое качественное фото
                photo = update["message"]["photo"][-1]
                photo_file_id = photo["file_id"]
                photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={photo_file_id}"
                
                response = await ai_engine.handle_image_message(photo_url, user_id)
                await send_telegram_message(chat_id, response, menu=True)
            
            # 💬 ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ
            elif "text" in update["message"]:
                text = update["message"]["text"].strip()
                
                if text.startswith("/start"):
                    response = "🚀 **SuperAi+ ТУРБО-РЕЖИМ!**\n\n💎 _Все функции активированы_\n🎯 _Интеллектуальные ответы_\n⚡ _Работаю 24/7_\n\n👇 **Используйте меню ниже:**"
                    await send_telegram_message(chat_id, response, menu=True)
                
                elif text.startswith("/help"):
                    response = ai_engine._help_response()
                    await send_telegram_message(chat_id, response, menu=True)
                
                elif text.startswith("/decompose"):
                    goal = text.replace("/decompose", "").strip()
                    if goal:
                        response = await ai_engine.decompose_goal(goal, user_id)
                    else:
                        response = "🎯 Напишите цель после команды /decompose\n\nПример: /decompose Выучить английский язык"
                    await send_telegram_message(chat_id, response, menu=True)
                
                elif text.startswith("/menu"):
                    await send_telegram_message(chat_id, "🔄 **Меню обновлено!**", menu=True)
                
                # 🔥 ОБРАБОТКА ЛЮБЫХ СООБЩЕНИЙ С МЕНЮ
                else:
                    response = ai_engine.get_intelligent_response(text, user_id)
                    await send_telegram_message(chat_id, response, menu=True)
                
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    
    return {"status": "ok"}

async def send_telegram_message(chat_id: int, text: str, menu: bool = False):
    """Отправка сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    # 🔥 ВСЕГДА показываем меню (кроме особых случаев)
    if menu:
        payload["reply_markup"] = json.dumps(MENU_KEYBOARD)
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        logger.info(f"Message sent to {chat_id}")
        return response.json()
    except Exception as e:
        logger.error(f"Send message error: {e}")

@app.get("/")
async def root():
    return {
        "status": "SuperAi+ ULTRA работает!",
        "version": "5.0",
        "features": [
            "Голосовой интерфейс (STT/TTS)",
            "Анализ изображений (Vision AI)", 
            "Декомпозитор целей (DeepSeek AI)",
            "Кристаллы памяти",
            "Система нейронов",
            "P2P маркетплейс"
        ]
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья сервера"""
    return {"status": "healthy", "timestamp": time.time()}

# 🔧 АВТО-ПИНГЕР ДЛЯ RENDER
import threading
def keep_alive():
    while True:
        try:
            requests.get("https://new-era-ai-bot.onrender.com/health", timeout=10)
        except:
            pass
        time.sleep(300)  # 5 минут

# Запуск авто-пингерав фоне
threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000, access_log=False)
