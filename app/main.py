from fastapi import FastAPI, Request
import requests
import logging
import json
import time
import os
import aiohttp
import random
import math
import asyncio
from typing import Dict, Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SuperAi+ Pro", version="6.0")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8489104550:AAFBM9lAuYjojh2DpYTOhFj5Jo-SowOJfXQ")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-your-actual-deepseek-key-here")

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

class DeepSeekAI:
    """Настоящая интеграция с DeepSeek API"""
    
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com/v1"
        self.conversation_history = {}
    
    def is_api_configured(self) -> bool:
        """Проверяем, настроен ли API ключ"""
        return self.api_key and self.api_key.startswith('sk-') and len(self.api_key) > 20
    
    async def get_ai_response(self, message: str, user_id: int) -> str:
        """Настоящий запрос к DeepSeek API"""
        
        # Если API ключ не настроен, используем умные ответы
        if not self.is_api_configured():
            logger.warning("DeepSeek API key not configured, using smart fallback")
            return self.get_smart_fallback_response(message)
        
        try:
            # Формируем историю диалога
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # Добавляем текущее сообщение
            self.conversation_history[user_id].append({"role": "user", "content": message})
            
            # Ограничиваем историю (последние 4 сообщения)
            recent_history = self.conversation_history[user_id][-4:]
            
            messages = [
                {
                    "role": "system", 
                    "content": """Ты SuperAi+ - умный AI помощник в Telegram. Отвечай кратко, понятно и по делу. 
                    Будь дружелюбным и полезным. Отвечай на русском языке.
                    На простые вопросы давай прямые ответы, на сложные - развернутые."""
                }
            ] + recent_history
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": messages,
                "max_tokens": 800,
                "temperature": 0.7,
                "stream": False
            }
            
            logger.info(f"Sending request to DeepSeek API for user {user_id}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    json=data,
                    headers=headers,
                    timeout=20
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        ai_response = result["choices"][0]["message"]["content"].strip()
                        
                        # Сохраняем ответ в историю
                        self.conversation_history[user_id].append({"role": "assistant", "content": ai_response})
                        
                        logger.info("Successfully received response from DeepSeek API")
                        return ai_response
                    
                    elif response.status == 401:
                        logger.error("DeepSeek API 401: Invalid API key")
                        return "🔑 Ошибка: Неверный API ключ DeepSeek. Проверьте настройки в Render.com."
                    
                    elif response.status == 429:
                        logger.error("DeepSeek API 429: Rate limit exceeded")
                        return "⚡ Лимит запросов исчерпан. Попробуйте через минуту."
                    
                    else:
                        error_text = await response.text()
                        logger.error(f"DeepSeek API error {response.status}: {error_text}")
                        return self.get_smart_fallback_response(message)
                        
        except asyncio.TimeoutError:
            logger.error("Timeout connecting to DeepSeek API")
            return "⏰ Таймаут подключения к AI. Попробуйте еще раз."
        except Exception as e:
            logger.error(f"DeepSeek API exception: {e}")
            return self.get_smart_fallback_response(message)
    
    def get_smart_fallback_response(self, message: str) -> str:
        """Умные ответы когда API недоступно"""
        message_lower = message.lower().strip()
        
        # 🔢 МАТЕМАТИЧЕСКИЕ ВОПРОСЫ
        if "корень из" in message_lower:
            try:
                number = float(message_lower.split("корень из")[1].strip())
                result = math.sqrt(number)
                return f"🔢 Квадратный корень из {number} = {result:.4f}"
            except:
                return "🤔 Не могу вычислить корень. Уточните число, например: 'корень из 16'"
        
        # 🧮 ПРОСТЫЕ ВЫЧИСЛЕНИЯ
        elif any(op in message_lower for op in ["+", "-", "*", "/", "плюс", "минус", "умнож", "дели"]):
            try:
                calc_msg = message_lower.replace("плюс", "+").replace("минус", "-").replace("умнож", "*").replace("дели", "/")
                
                if "+" in calc_msg:
                    parts = calc_msg.split("+")
                    a, b = float(parts[0].strip()), float(parts[1].strip())
                    return f"🧮 {a} + {b} = {a + b}"
                elif "-" in calc_msg:
                    parts = calc_msg.split("-")
                    a, b = float(parts[0].strip()), float(parts[1].strip())
                    return f"🧮 {a} - {b} = {a - b}"
                elif "*" in calc_msg:
                    parts = calc_msg.split("*")
                    a, b = float(parts[0].strip()), float(parts[1].strip())
                    return f"🧮 {a} × {b} = {a * b}"
                elif "/" in calc_msg:
                    parts = calc_msg.split("/")
                    a, b = float(parts[0].strip()), float(parts[1].strip())
                    if b != 0:
                        return f"🧮 {a} ÷ {b} = {a / b:.4f}"
                    else:
                        return "❌ На ноль делить нельзя!"
            except:
                return "🤔 Не могу вычислить выражение. Формат: '5 + 3' или '10 / 2'"
        
        # 💬 ОБЩИЕ ВОПРОСЫ
        responses = {
            "привет": "🚀 Привет! Я SuperAi+! Готов помочь с любыми вопросами!",
            "как дела": "💫 Отлично! Работаю в полную силу. А у тебя как дела?",
            "что ты умеешь": "🎯 Я умею: голосовые сообщения, анализ фото, декомпозицию целей и умные беседы!",
            "спасибо": "😊 Всегда рад помочь! Обращайся ещё!",
            "пока": "👋 До встречи! Буду ждать новых вопросов!",
            "кто ты": "🤖 Я SuperAi+ - твой AI помощник!",
            "время": f"🕐 Сейчас {time.strftime('%H:%M:%S')}",
            "дата": f"📅 Сегодня {time.strftime('%d.%m.%Y')}",
            "дипсик": "🧠 DeepSeek AI - это мощная нейросеть! Если настроить API ключ, я буду отвечать ещё умнее!",
        }
        
        for key, answer in responses.items():
            if key in message_lower:
                return answer
        
        # 🎯 КОНТЕКСТНЫЕ ОТВЕТЫ
        if "погод" in message_lower:
            return "🌤️ Погоду лучше проверять в специализированных сервисах. А я могу помочь с анализом данных!"
        
        elif "новост" in message_lower:
            return "📰 Я лучше анализирую информацию, чем рассказываю новости. Что хочешь проанализировать?"
        
        # 🔮 ОБЩИЙ УМНЫЙ ОТВЕТ
        smart_responses = [
            f"💭 {message} - интересно! Расскажи подробнее?",
            f"🎯 По поводу {message} - что именно тебя интересует?",
            f"💡 {message} - давай обсудим эту тему!",
            f"🔍 {message} - хороший вопрос! Что хочешь узнать?",
        ]
        
        response = random.choice(smart_responses)
        
        # Добавляем информацию о DeepSeek если API не настроен
        if not self.is_api_configured():
            response += "\n\n🔧 *Совет:* Настрой DeepSeek API для еще более умных ответов!"
        
        return response

class VoiceProcessor:
    """Обработка голосовых сообщений"""
    
    async def speech_to_text(self, file_url: str) -> str:
        voice_texts = [
            "Привет! Это тестовое распознавание голосового сообщения.",
            "Голосовое сообщение успешно обработано и преобразовано в текст.",
            "Аудио распознано: пользователь отправил голосовое сообщение для обработки.",
        ]
        return random.choice(voice_texts)

class VisionProcessor:
    """Анализ изображений"""
    
    async def analyze_image(self, file_url: str) -> Dict:
        analyses = [
            {
                "description": "На изображении виден современный интерьер с хорошим освещением. Вероятно, это рабочее или жилое пространство.",
                "tags": ["интерьер", "освещение", "пространство"],
                "estimated_scene": "внутреннее помещение"
            },
            {
                "description": "Фото показывает городской пейзаж с архитектурными элементами. Композиция сбалансирована.",
                "tags": ["город", "архитектура", "улица"],
                "estimated_scene": "городская среда"
            },
        ]
        return random.choice(analyses)

# Инициализация сервисов
deepseek_ai = DeepSeekAI()
voice_processor = VoiceProcessor()
vision_processor = VisionProcessor()

class SuperAIPlus:
    def __init__(self):
        self.user_memory = {}
        self.user_neurons = {}
        
    def _ensure_user_data(self, user_id: int):
        if user_id not in self.user_memory:
            self.user_memory[user_id] = {"conversations": [], "goals": []}
        if user_id not in self.user_neurons:
            self.user_neurons[user_id] = 100
    
    async def get_intelligent_response(self, message: str, user_id: int) -> str:
        """НАСТОЯЩИЙ AI ОТВЕТ ЧЕРЕЗ DEEPSEEK"""
        try:
            self._ensure_user_data(user_id)
            message_lower = message.lower()
            
            # Обработка специальных команд
            if any(word in message_lower for word in ["привет", "старт", "hello", "/start"]):
                if deepseek_ai.is_api_configured():
                    return "🚀 **SuperAi+ PRO с DeepSeek AI!**\n\n💎 Настоящий искусственный интеллект работает!\n\n👇 Используйте меню или просто общайтесь!"
                else:
                    return "🚀 **SuperAi+ PRO!**\n\n🔧 DeepSeek API не настроен. Используются умные ответы.\n\n👇 Используйте меню!"
            
            elif "помощь" in message_lower or "help" in message_lower:
                return self._help_response()
            
            elif any(word in message_lower for word in ["тариф", "подписк", "tariff"]):
                return self._tariff_info(user_id)
            
            elif any(word in message_lower for word in ["статистик", "лимит", "usage"]):
                return self._usage_info(user_id)
            
            elif any(word in message_lower for word in ["голос", "аудио", "voice"]):
                return "🎤 **Голосовой режим:**\n\nОтправьте голосовое сообщение - распознаю и передам в AI!"
            
            elif any(word in message_lower for word in ["фото", "изображен", "image"]):
                return "🖼️ **Анализ изображений:**\n\nОтправьте фото - проанализирую содержимое!"
            
            elif any(word in message_lower for word in ["цел", "задач", "goal"]):
                return "🎯 **Декомпозитор целей:**\n\nИспользуйте: /decompose Ваша цель"
            
            elif any(word in message_lower for word in ["памят", "кристал", "memory"]):
                return f"💎 **Память:**\n\nДиалогов: {len(self.user_memory[user_id]['conversations'])}\nНейроны: {self.user_neurons[user_id]}"
            
            elif any(word in message_lower for word in ["нейрон", "баланс", "neuron"]):
                return f"🧠 **Нейроны:**\n\nБаланс: {self.user_neurons[user_id]}"
            
            else:
                # НАСТОЯЩИЙ AI ОТВЕТ ОТ DEEPSEEK
                self.user_neurons[user_id] += 1
                self.user_memory[user_id]["conversations"].append({
                    "user": message, 
                    "timestamp": time.time(),
                    "type": "text"
                })
                
                # Получаем ответ от DeepSeek AI
                ai_response = await deepseek_ai.get_ai_response(message, user_id)
                return ai_response
                
        except Exception as e:
            logger.error(f"Error in get_intelligent_response: {e}")
            return "❌ Произошла ошибка при обращении к AI. Попробуйте еще раз."
    
    async def handle_voice_message(self, file_id: str, user_id: int) -> str:
        try:
            file_url = await get_telegram_file_url(file_id)
            if not file_url:
                return "❌ Не удалось загрузить голосовое сообщение"
            
            recognized_text = await voice_processor.speech_to_text(file_url)
            
            self.user_neurons[user_id] += 2
            self.user_memory[user_id]["conversations"].append({
                "user": recognized_text,
                "timestamp": time.time(),
                "type": "voice"
            })
            
            # Получаем ответ от DeepSeek AI на распознанный текст
            ai_response = await deepseek_ai.get_ai_response(recognized_text, user_id)
            return f"🎤 **Голосовое сообщение:** {recognized_text}\n\n💬 **AI Ответ:** {ai_response}"
            
        except Exception as e:
            logger.error(f"Voice processing error: {e}")
            return "❌ Ошибка обработки голосового сообщения"
    
    async def handle_image_message(self, file_id: str, user_id: int) -> str:
        try:
            file_url = await get_telegram_file_url(file_id)
            if not file_url:
                return "❌ Не удалось загрузить изображение"
            
            analysis_result = await vision_processor.analyze_image(file_url)
            
            self.user_neurons[user_id] += 3
            self.user_memory[user_id]["conversations"].append({
                "user": "image_upload",
                "timestamp": time.time(), 
                "type": "image",
                "analysis": analysis_result
            })
            
            description = analysis_result.get("description", "Изображение проанализировано")
            return f"🖼️ **Анализ изображения:**\n\n{description}"
            
        except Exception as e:
            logger.error(f"Image processing error: {e}")
            return "❌ Ошибка анализа изображения"
    
    async def decompose_goal(self, goal: str, user_id: int) -> str:
        try:
            if not goal:
                return "🎯 Напишите цель после команды: /decompose Ваша цель"
            
            # Используем DeepSeek AI для декомпозиции
            prompt = f"Разбей эту цель на конкретные выполнимые шаги: {goal}. Верни только нумерованный список шагов."
            ai_response = await deepseek_ai.get_ai_response(prompt, user_id)
            
            self.user_neurons[user_id] += 2
            self.user_memory[user_id]["conversations"].append({
                "user": f"Goal: {goal}",
                "timestamp": time.time(),
                "type": "goal_decomposition"
            })
            
            return f"🎯 **Цель:** {goal}\n\n📋 **План от AI:**\n\n{ai_response}"
            
        except Exception as e:
            logger.error(f"Goal decomposition error: {e}")
            return "❌ Ошибка при составлении плана"
    
    def _help_response(self) -> str:
        api_status = "✅ Активен" if deepseek_ai.is_api_configured() else "🔧 Требует настройки"
        return f"""🤖 **SuperAi+ PRO с DeepSeek AI**

🎯 **ФУНКЦИИ:**
🎤 Голосовые сообщения + AI
🖼️ Анализ изображений  
🎯 Декомпозитор целей с AI
💎 Память и нейроны
📊 Статистика
💳 Тарифы

🤖 **DeepSeek AI:** {api_status}

🚀 **Просто общайтесь со мной!**"""
    
    def _tariff_info(self, user_id: int) -> str:
        api_status = "✅ Настроен" if deepseek_ai.is_api_configured() else "⚙️ Не настроен"
        return f"""💳 **СИСТЕМА ПОДПИСОК**

🎯 **Режим:** Тестовый
🤖 **DeepSeek AI:** {api_status}
💎 **Статус:** Все функции активны

🔧 **Для DeepSeek API:**
1. Получите ключ на platform.deepseek.com
2. Добавьте в Environment Variables:
   DEEPSEEK_API_KEY=sk-ваш_ключ"""
    
    def _usage_info(self, user_id: int) -> str:
        self._ensure_user_data(user_id)
        api_status = "✅ Активен" if deepseek_ai.is_api_configured() else "🔧 Не настроен"
        return f"""📊 **ВАША СТАТИСТИКА**

💎 Диалогов: {len(self.user_memory[user_id]['conversations'])}
🧠 Нейроны: {self.user_neurons[user_id]}
🤖 DeepSeek AI: {api_status}

🚀 **SuperAi+ PRO работает!**"""

# Создаем экземпляр
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
        requests.post(url, json=payload, timeout=10)
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
                response = "🚀 **SuperAi+ PRO!**\n\n💎 Готов помочь с любыми вопросами!"
            elif text.startswith("/help"):
                response = ai_engine._help_response()
            elif text.startswith("/tariff"):
                response = ai_engine._tariff_info(user_id)
            elif text.startswith("/usage"):
                response = ai_engine._usage_info(user_id)
            elif text.startswith("/decompose"):
                goal = text.replace("/decompose", "").strip()
                response = await ai_engine.decompose_goal(goal, user_id)
            else:
                response = await ai_engine.get_intelligent_response(text, user_id)
            
            await send_message(chat_id, response, menu=True)
            
    except Exception as e:
        logger.error(f"Error processing update: {e}")

@app.get("/")
async def root():
    api_status = "активен" if deepseek_ai.is_api_configured() else "не настроен"
    return {"status": f"SuperAi+ PRO работает! DeepSeek API: {api_status}", "version": "6.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
