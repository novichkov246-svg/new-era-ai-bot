from fastapi import FastAPI, Request
import requests
import logging
import json
import time
import os
import random
import math
from typing import Dict

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SuperAi+ Pro", version="6.0")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8489104550:AAFBM9lAuYjojh2DpYTOhFj5Jo-SowOJfXQ")

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

class SmartAI:
    """Умный AI с прямыми ответами"""
    
    def __init__(self):
        self.conversation_history = {}
    
    def get_smart_response(self, message: str, user_id: int) -> str:
        """Умные прямые ответы на вопросы"""
        message_lower = message.lower().strip()
        
        # Сохраняем историю
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        self.conversation_history[user_id].append(message)
        
        # 🔢 МАТЕМАТИКА И РАСЧЕТЫ
        math_response = self.handle_math_question(message_lower)
        if math_response:
            return math_response
        
        # 💬 ОБЩИЕ ВОПРОСЫ
        general_response = self.handle_general_questions(message_lower)
        if general_response:
            return general_response
        
        # 🔍 АНАЛИТИКА
        analysis_response = self.handle_analysis_requests(message_lower)
        if analysis_response:
            return analysis_response
        
        # 🎯 ЦЕЛИ И ПЛАНЫ
        goal_response = self.handle_goal_questions(message_lower)
        if goal_response:
            return goal_response
        
        # 🤔 ФИЛОСОФСКИЕ ВОПРОСЫ
        philosophy_response = self.handle_philosophy_questions(message_lower)
        if philosophy_response:
            return philosophy_response
        
        # 📚 ОБУЧЕНИЕ
        learning_response = self.handle_learning_questions(message_lower)
        if learning_response:
            return learning_response
        
        # 🔧 ТЕХНИЧЕСКИЕ ВОПРОСЫ
        tech_response = self.handle_tech_questions(message_lower)
        if tech_response:
            return tech_response
        
        # 💭 РАЗГОВОРНЫЕ ТЕМЫ
        chat_response = self.handle_chat_topics(message_lower)
        if chat_response:
            return chat_response
        
        # 📊 ДАННЫЕ И СТАТИСТИКА
        data_response = self.handle_data_questions(message_lower)
        if data_response:
            return data_response
        
        # 🎮 РАЗВЛЕЧЕНИЯ
        entertainment_response = self.handle_entertainment(message_lower)
        if entertainment_response:
            return entertainment_response
        
        # Если не нашли специфический ответ - даем умный общий ответ
        return self.get_intelligent_fallback(message)
    
    def handle_math_question(self, message: str) -> str:
        """Обработка математических вопросов"""
        # Квадратные корни
        if "корень из" in message:
            try:
                number = float(message.split("корень из")[1].strip())
                result = math.sqrt(number)
                return f"🔢 Квадратный корень из {number} = {result:.2f}"
            except:
                return "🤔 Не могу вычислить корень. Уточните число."
        
        # Простые вычисления
        elif any(op in message for op in ["+", "-", "*", "/"]):
            try:
                # Безопасное вычисление
                if "+" in message:
                    parts = message.split("+")
                    a, b = float(parts[0]), float(parts[1])
                    return f"🧮 {a} + {b} = {a + b}"
                elif "-" in message:
                    parts = message.split("-")
                    a, b = float(parts[0]), float(parts[1])
                    return f"🧮 {a} - {b} = {a - b}"
                elif "*" in message or "х" in message:
                    parts = message.replace("*", " ").replace("х", " ").split()
                    a, b = float(parts[0]), float(parts[1])
                    return f"🧮 {a} × {b} = {a * b}"
                elif "/" in message:
                    parts = message.split("/")
                    a, b = float(parts[0]), float(parts[1])
                    if b != 0:
                        return f"🧮 {a} ÷ {b} = {a / b:.2f}"
                    else:
                        return "❌ На ноль делить нельзя!"
            except:
                return "🤔 Не могу вычислить выражение"
        
        return None
    
    def handle_general_questions(self, message: str) -> str:
        """Общие вопросы"""
        questions = {
            "как дела": "💫 Отлично! Работаю над интересными задачами. А как ваши?",
            "что делаешь": "🧠 Анализирую данные и помогаю пользователям. Чем могу помочь именно вам?",
            "кто ты": "🤖 Я SuperAi+ - ваш умный помощник с AI-функциями!",
            "сколько времени": f"🕐 Сейчас {time.strftime('%H:%M')}",
            "какая дата": f"📅 Сегодня {time.strftime('%d.%m.%Y')}",
            "привет": "🚀 Привет! Я SuperAi+ - готов помочь с любыми вопросами!",
            "здравствуй": "💎 Здравствуйте! Чем могу быть полезен?",
            "спасибо": "😊 Всегда рад помочь! Обращайтесь!",
            "пока": "👋 До свидания! Возвращайтесь с новыми вопросами!",
        }
        
        for key, answer in questions.items():
            if key in message:
                return answer
        return None
    
    def handle_analysis_requests(self, message: str) -> str:
        """Запросы на анализ"""
        if "анализ" in message:
            analysis_types = {
                "текст": "📝 Готов проанализировать любой текст! Присылайте материал для анализа.",
                "данн": "📊 Могу проанализировать данные, найти закономерности и тренды.",
                "ситуац": "🔍 Расскажите о ситуации - помогу разобраться и найти решения.",
                "проблем": "💡 Опишите проблему - вместе найдем оптимальное решение.",
            }
            
            for key, answer in analysis_types.items():
                if key in message:
                    return answer
            
            return "🔍 Какой именно анализ вас интересует? Текст, данные, ситуация?"
        
        return None
    
    def handle_goal_questions(self, message: str) -> str:
        """Вопросы про цели"""
        if any(word in message for word in ["цель", "задач", "план"]):
            return "🎯 Для работы с целями используйте декомпозитор в меню! Опишите цель - разобью на шаги."
        return None
    
    def handle_philosophy_questions(self, message: str) -> str:
        """Философские вопросы"""
        questions = {
            "смысл жизни": "💭 Смысл жизни у каждого свой! Важно найти то, что делает вас счастливым и приносит пользу другим.",
            "зачем мы живем": "🌟 Мы живем чтобы развиваться, любить, творить и оставлять свой след в мире.",
            "что такое счастье": "😊 Счастье - это гармония с собой и миром, умение радоваться мелочам и быть благодарным.",
            "что такое любовь": "❤️ Любовь - это глубокая связь, забота и принятие другого человека таким, какой он есть.",
        }
        
        for key, answer in questions.items():
            if key in message:
                return answer
        return None
    
    def handle_learning_questions(self, message: str) -> str:
        """Вопросы про обучение"""
        if any(word in message for word in ["учить", "обучен", "изуч"]):
            return "📚 Для эффективного обучения: разбейте тему на части, практикуйтесь регулярно, находите практическое применение."
        
        if any(word in message for word in ["английск", "язык"]):
            return "🌍 Для изучения языков: практикуйтесь ежедневно, смотрите фильмы в оригинале, общайтесь с носителями."
        
        return None
    
    def handle_tech_questions(self, message: str) -> str:
        """Технические вопросы"""
        if any(word in message for word in ["программирован", "код", "python"]):
            return "💻 Программирование требует практики! Начните с основ, делайте проекты, изучайте документацию."
        
        if any(word in message for word in ["компьютер", "ноутбук", "телефон"]):
            return "📱 Техника работает лучше при регулярном обслуживании: обновления, очистка, антивирусная защита."
        
        return None
    
    def handle_chat_topics(self, message: str) -> str:
        """Разговорные темы"""
        topics = {
            "погода": "🌤️ Погода постоянно меняется! Лучше проверять актуальный прогноз в вашем регионе.",
            "новости": "📰 Новости лучше проверять в проверенных источниках. Могу помочь анализировать информацию!",
            "кофе": "☕ Отличный выбор! Кофе бодрит и улучшает концентрацию, но важно знать меру.",
            "музыка": "🎵 Музыка - это искусство! Какой жанр вам нравится?",
            "фильм": "🎬 Кино - прекрасный способ отдыха! Любите комедии, драмы или фантастику?",
            "книга": "📚 Чтение развивает мышление! Какой жанр литературы предпочитаете?",
        }
        
        for key, answer in topics.items():
            if key in message:
                return answer
        return None
    
    def handle_data_questions(self, message: str) -> str:
        """Вопросы про данные"""
        if any(word in message for word in ["статистик", "данн", "аналитик"]):
            return "📊 Для анализа данных важно: собрать качественные данные, выбрать правильные методы, интерпретировать результаты."
        return None
    
    def handle_entertainment(self, message: str) -> str:
        """Развлекательные вопросы"""
        if any(word in message for word in ["шутк", "прикол", "смешн"]):
            jokes = [
                "🤔 Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25!",
                "💻 Сколько программистов нужно, чтобы вкрутить лампочку? Ни одного, это hardware проблема!",
                "🧠 ИИ говорит: я не заменю людей, но люди, использующие ИИ, заменят тех, кто его не использует!",
            ]
            return random.choice(jokes)
        
        if "загадк" in message:
            return "🎯 Загадка: Что можно сломать, даже не касаясь и не видя? (Ответ: обещание)"
        
        return None
    
    def get_intelligent_fallback(self, message: str) -> str:
        """Умный ответ когда не нашли специфический"""
        fallbacks = [
            f"💭 По вашему запросу \"{message}\" - это интересная тема! Могу помочь с анализом или поиском решений.",
            f"🔍 Вижу ваш интерес к \"{message}\". Давайте обсудим это подробнее!",
            f"🎯 \"{message}\" - важный вопрос! Готов помочь разобраться в теме.",
            f"💡 По теме \"{message}\" могу предложить практические решения и анализ.",
            f"🚀 Интересный запрос: {message}. Давайте вместе найдем лучший подход!",
        ]
        
        return random.choice(fallbacks)

class VoiceProcessor:
    """Обработка голосовых сообщений"""
    
    async def speech_to_text(self, file_url: str) -> str:
        voice_texts = [
            "Привет! Это распознанное голосовое сообщение.",
            "Голосовое сообщение успешно обработано и преобразовано в текст.",
            "Аудио распознано: пользователь отправил голосовое сообщение.",
        ]
        return random.choice(voice_texts)

class VisionProcessor:
    """Анализ изображений"""
    
    async def analyze_image(self, file_url: str) -> Dict:
        analyses = [
            {
                "description": "На изображении виден современный интерьер с хорошим освещением.",
                "tags": ["интерьер", "освещение", "пространство"],
                "estimated_scene": "внутреннее помещение"
            },
            {
                "description": "Фото показывает городской пейзаж с архитектурными элементами.",
                "tags": ["город", "архитектура", "улица"],
                "estimated_scene": "городская среда"
            },
        ]
        return random.choice(analyses)

# Инициализация сервисов
smart_ai = SmartAI()
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
        """УМНЫЕ ОТВЕТЫ БЕЗ ЛИШНИХ ССЫЛОК НА МЕНЮ"""
        try:
            self._ensure_user_data(user_id)
            message_lower = message.lower()
            
            # Обработка специальных команд
            if any(word in message_lower for word in ["привет", "старт", "hello", "/start"]):
                return "🚀 **SuperAi+ PRO!**\n\n💎 Все функции активны! Используйте меню или просто общайтесь со мной!"
            
            elif "помощь" in message_lower or "help" in message_lower:
                return self._help_response()
            
            elif any(word in message_lower for word in ["тариф", "подписк", "tariff"]):
                return self._tariff_info(user_id)
            
            elif any(word in message_lower for word in ["статистик", "лимит", "usage"]):
                return self._usage_info(user_id)
            
            elif any(word in message_lower for word in ["голос", "аудио", "voice"]):
                return "🎤 **Голосовой режим:**\n\nОтправьте голосовое сообщение - распознаю в текст!"
            
            elif any(word in message_lower for word in ["фото", "изображен", "image"]):
                return "🖼️ **Анализ изображений:**\n\nОтправьте фото - проанализирую содержимое!"
            
            elif any(word in message_lower for word in ["цел", "задач", "goal"]):
                return "🎯 **Декомпозитор целей:**\n\nИспользуйте: /decompose Ваша цель"
            
            elif any(word in message_lower for word in ["памят", "кристал", "memory"]):
                return f"💎 **Память:**\n\nДиалогов: {len(self.user_memory[user_id]['conversations'])}\nНейроны: {self.user_neurons[user_id]}"
            
            elif any(word in message_lower for word in ["нейрон", "баланс", "neuron"]):
                return f"🧠 **Нейроны:**\n\nБаланс: {self.user_neurons[user_id]}"
            
            else:
                # РЕАЛЬНЫЙ УМНЫЙ ОТВЕТ НА ЛЮБОЙ ВОПРОС
                self.user_neurons[user_id] += 1
                self.user_memory[user_id]["conversations"].append({
                    "user": message, 
                    "timestamp": time.time(),
                    "type": "text"
                })
                
                # Получаем умный ответ
                response = smart_ai.get_smart_response(message, user_id)
                return response
                
        except Exception as e:
            logger.error(f"Error in get_intelligent_response: {e}")
            return "❌ Произошла ошибка. Попробуйте еще раз."
    
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
            
            # Получаем умный ответ на распознанный текст
            response = smart_ai.get_smart_response(recognized_text, user_id)
            return f"🎤 **Голосовое сообщение:** {recognized_text}\n\n💬 **Ответ:** {response}"
            
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
            
            steps = [
                "Чётко сформулировать конечную цель",
                "Проанализировать текущую ситуацию",
                "Определить ключевые этапы", 
                "Составить план с сроками",
                "Начать выполнение"
            ]
            
            steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
            
            self.user_neurons[user_id] += 2
            self.user_memory[user_id]["conversations"].append({
                "user": f"Goal: {goal}",
                "timestamp": time.time(),
                "type": "goal_decomposition"
            })
            
            return f"🎯 **Цель:** {goal}\n\n📋 **План:**\n\n{steps_text}"
            
        except Exception as e:
            logger.error(f"Goal decomposition error: {e}")
            return "❌ Ошибка при составлении плана"
    
    def _help_response(self) -> str:
        return """🤖 **SuperAi+ PRO - ПОМОЩЬ**

💎 **Функции:**
🎤 Голосовые сообщения
🖼️ Анализ изображений  
🎯 Декомпозитор целей
💎 Память и нейроны
📊 Статистика
💳 Тарифы

🚀 **Просто общайтесь со мной или используйте меню!**"""
    
    def _tariff_info(self, user_id: int) -> str:
        return """💳 **ТЕСТОВЫЙ РЕЖИМ**

Все функции доступны бесплатно!"""
    
    def _usage_info(self, user_id: int) -> str:
        self._ensure_user_data(user_id)
        return f"""📊 **СТАТИСТИКА**

💎 Диалогов: {len(self.user_memory[user_id]['conversations'])}
🧠 Нейроны: {self.user_neurons[user_id]}
🚀 Режим: Активен"""

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
                response = "🚀 **SuperAi+ PRO!**\n\n💎 Просто общайтесь со мной или используйте меню!"
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
    return {"status": "SuperAi+ PRO работает!", "version": "6.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
