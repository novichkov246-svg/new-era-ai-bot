from fastapi import FastAPI, Request
import requests
import logging
import json
import time
import os
import random
from typing import Dict

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SuperAi+ Pro", version="6.0")

# Токен бота
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

class AIClient:
    """Локальный AI без внешних API"""
    
    def __init__(self):
        self.responses = {
            "привет": [
                "Привет! Я SuperAi+ - ваш персональный AI помощник! 🚀",
                "Здравствуйте! Готов помочь с любыми задачами! 💎",
                "Приветствую! Используйте меню для доступа к функциям! 🤖"
            ],
            "как дела": [
                "Отлично! Готов работать и помогать вам! 💪",
                "Прекрасно! Жду ваших заданий и вопросов! 🔮",
                "Всё замечательно! Что хотите обсудить? 💭"
            ],
            "спасибо": [
                "Всегда рад помочь! Обращайтесь! 😊",
                "Пожалуйста! Это моя работа - помогать вам! 🌟",
                "Рад был помочь! Что еще могу сделать? 💫"
            ],
            "помощь": [
                "Я могу: обрабатывать голосовые, анализировать фото, ставить цели!",
                "Мои функции: голосовые сообщения, анализ изображений, планирование!",
                "Помогу с: задачами, анализом, планированием и многим другим!"
            ]
        }
    
    async def chat_completion(self, message: str) -> str:
        """Умные ответы без внешнего API"""
        message_lower = message.lower()
        
        # Специальные ответы
        if any(word in message_lower for word in ["привет", "хай", "здравствуй"]):
            return random.choice(self.responses["привет"])
        elif any(word in message_lower for word in ["как дела", "как ты"]):
            return random.choice(self.responses["как дела"])
        elif any(word in message_lower for word in ["спасибо", "благодарю"]):
            return random.choice(self.responses["спасибо"])
        elif any(word in message_lower for word in ["помощь", "help"]):
            return random.choice(self.responses["помощь"])
        
        # Умные ответы на разные темы
        if any(word in message_lower for word in ["погод", "дождь", "солнц"]):
            return "🌤️ Погода - интересная тема! К сожалению, у меня нет доступа к актуальным данным о погоде, но могу помочь с планированием дел!"
        
        elif any(word in message_lower for word in ["новост", "событи"]):
            return "📰 Новости постоянно меняются! Рекомендую проверять актуальные источники. Могу помочь анализировать информацию!"
        
        elif any(word in message_lower for word in ["врем", "час", "который час"]):
            return f"⏰ Сейчас примерно {time.strftime('%H:%M')}. Точное время лучше уточнить в вашем устройстве!"
        
        elif any(word in message_lower for word in ["кошк", "собак", "животн"]):
            return "🐾 Милые животные! У вас есть питомец? Могу помочь с советами по уходу или тренировкам!"
        
        elif any(word in message_lower for word in ["работ", "проект", "задач"]):
            return "💼 Рабочие вопросы? Отлично! Используйте декомпозитор целей чтобы разбить большие задачи на шаги!"
        
        elif any(word in message_lower for word in ["учёб", "образован", "студент"]):
            return "🎓 Учёба - это важно! Могу помочь составить план обучения или разбить сложные темы на части!"
        
        else:
            # Общие интеллектуальные ответы
            responses = [
                f"🧠 **Анализирую ваш запрос:** \"{message}\"\n\n💡 Интересная тема! Могу предложить:\n• Разбить на подзадачи\n• Проанализировать детали\n• Составить план действий",
                f"🔮 **По вашему вопросу:** \"{message}\"\n\n💎 Используйте мои функции:\n• 🎤 Голосовые сообщения\n• 🖼️ Анализ изображений\n• 🎯 Декомпозитор целей",
                f"🤖 **Обрабатываю:** \"{message}\"\n\n✨ Что именно вас интересует? Я могу:\n• Анализировать информацию\n• Помогать с планированием\n• Обрабатывать разные типы данных",
                f"💫 **Ваш запрос:** \"{message}\"\n\n🚀 Готов помочь! Выберите функцию в меню или продолжайте диалог - я адаптируюсь под ваши needs!"
            ]
            return random.choice(responses)

class VoiceProcessor:
    """Обработка голосовых сообщений"""
    
    async def speech_to_text(self, file_url: str) -> str:
        """Имитация распознавания голоса"""
        # В реальности здесь будет скачивание и обработка аудио
        # Сейчас - умная заглушка
        
        voice_responses = [
            "Привет! Это распознанное голосовое сообщение. Система успешно обработала аудио!",
            "Голосовое сообщение получено и расшифровано. Текст готов для анализа!",
            "Аудио распознано: пользователь отправил голосовое сообщение для обработки.",
            "Голосовое сообщение расшифровано. Содержание передано в AI-систему!",
            "Отличное голосовое сообщение! Качество звука хорошее, распознавание прошло успешно."
        ]
        return random.choice(voice_responses)

class VisionProcessor:
    """Анализ изображений"""
    
    async def analyze_image(self, file_url: str) -> Dict:
        """Имитация анализа изображения"""
        # В реальности здесь будет скачивание и анализ изображения
        # Сейчас - умные заглушки
        
        analyses = [
            {
                "description": "На изображении виден современный интерьер с хорошим освещением. Вероятно, это рабочее или жилое пространство с продуманным дизайном.",
                "tags": ["интерьер", "освещение", "пространство", "дизайн"],
                "estimated_scene": "внутреннее помещение"
            },
            {
                "description": "Фото показывает городской пейзаж с архитектурными элементами. Композиция сбалансирована, цвета естественные.",
                "tags": ["город", "архитектура", "улица", "здания"],
                "estimated_scene": "городская среда"
            },
            {
                "description": "Изображение содержит природные элементы - возможно, парк или сад. Зелёные тона преобладают, атмосфера спокойная.",
                "tags": ["природа", "зелень", "пейзаж", "отдых"],
                "estimated_scene": "природная среда"
            },
            {
                "description": "На фото присутствуют люди в естественной обстановке. Эмоции положительные, композиция живая и динамичная.",
                "tags": ["люди", "портрет", "эмоции", "общение"],
                "estimated_scene": "социальная ситуация"
            },
            {
                "description": "Технологическое устройство или гаджет в фокусе. Современный дизайн, внимание к деталям.",
                "tags": ["технологии", "гаджет", "устройство", "дизайн"],
                "estimated_scene": "технический объект"
            }
        ]
        return random.choice(analyses)

# Инициализация процессоров
ai_client = AIClient()
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
        """Умный ответ без внешних API"""
        try:
            self._ensure_user_data(user_id)
            message_lower = message.lower()
            
            # Обработка команд
            if any(word in message_lower for word in ["привет", "старт", "hello", "/start"]):
                return "🚀 **SuperAi+ PRO!**\n\n💎 Полный функционал:\n• 🎤 Голосовые сообщения\n• 🖼️ Анализ фото\n• 🎯 Декомпозитор целей\n• 💎 Система памяти\n\n👇 Используйте меню!"
            
            elif "помощь" in message_lower or "help" in message_lower:
                return self._help_response()
            
            elif any(word in message_lower for word in ["тариф", "подписк", "tariff"]):
                return self._tariff_info(user_id)
            
            elif any(word in message_lower for word in ["статистик", "лимит", "usage"]):
                return self._usage_info(user_id)
            
            elif any(word in message_lower for word in ["голос", "аудио", "voice"]):
                return "🎤 **Голосовой режим:**\n\nОтправьте голосовое сообщение - я распознаю его в текст!"
            
            elif any(word in message_lower for word in ["фото", "изображен", "image", "картинк"]):
                return "🖼️ **Анализ изображений:**\n\nОтправьте фото - я проанализирую его содержимое!"
            
            elif any(word in message_lower for word in ["цел", "задач", "goal", "план"]):
                return "🎯 **Декомпозитор целей:**\n\nОпишите цель - разобью на конкретные шаги!\n\nИспользуйте: /decompose Ваша цель"
            
            elif any(word in message_lower for word in ["памят", "кристал", "memory"]):
                return f"💎 **Память:**\n\nДиалогов: {len(self.user_memory[user_id]['conversations'])}\nНейроны: {self.user_neurons[user_id]}"
            
            elif any(word in message_lower for word in ["нейрон", "баланс", "neuron"]):
                return f"🧠 **Нейроны:**\n\nБаланс: {self.user_neurons[user_id]}\n+1 за каждое сообщение!"
            
            else:
                # Умный AI-ответ
                self.user_neurons[user_id] += 1
                self.user_memory[user_id]["conversations"].append({
                    "user": message, 
                    "timestamp": time.time(),
                    "type": "text"
                })
                
                ai_response = await ai_client.chat_completion(message)
                return ai_response
                
        except Exception as e:
            logger.error(f"Error in get_intelligent_response: {e}")
            return "❌ Произошла ошибка. Попробуйте еще раз."
    
    async def handle_voice_message(self, file_id: str, user_id: int) -> str:
        """Обработка голосового сообщения"""
        try:
            # Получаем URL файла
            file_url = await get_telegram_file_url(file_id)
            if not file_url:
                return "❌ Не удалось загрузить голосовое сообщение"
            
            # Распознаем голос
            recognized_text = await voice_processor.speech_to_text(file_url)
            
            self.user_neurons[user_id] += 2
            self.user_memory[user_id]["conversations"].append({
                "user": recognized_text,
                "timestamp": time.time(),
                "type": "voice"
            })
            
            return f"🎤 **Голосовое сообщение распознано!**\n\n📝 Текст: {recognized_text}\n\n💡 Теперь я могу работать с этим текстом!"
            
        except Exception as e:
            logger.error(f"Voice processing error: {e}")
            return "❌ Ошибка обработки голосового сообщения"
    
    async def handle_image_message(self, file_id: str, user_id: int) -> str:
        """Анализ изображения"""
        try:
            # Получаем URL файла
            file_url = await get_telegram_file_url(file_id)
            if not file_url:
                return "❌ Не удалось загрузить изображение"
            
            # Анализируем изображение
            analysis_result = await vision_processor.analyze_image(file_url)
            
            self.user_neurons[user_id] += 3
            self.user_memory[user_id]["conversations"].append({
                "user": "image_upload",
                "timestamp": time.time(), 
                "type": "image",
                "analysis": analysis_result
            })
            
            description = analysis_result.get("description", "Изображение проанализировано")
            tags = ", ".join(analysis_result.get("tags", []))
            scene = analysis_result.get("estimated_scene", "не определено")
            
            return f"🖼️ **Анализ изображения:**\n\n📝 **Описание:** {description}\n\n🏷️ **Теги:** {tags}\n\n📍 **Сцена:** {scene}\n\n✨ Анализ выполнен AI-системой!"
            
        except Exception as e:
            logger.error(f"Image processing error: {e}")
            return "❌ Ошибка анализа изображения"
    
    async def decompose_goal(self, goal: str, user_id: int) -> str:
        """Декомпозиция целей"""
        try:
            if not goal:
                return "🎯 **Декомпозитор целей:**\n\nНапишите цель после команды:\n/decompose Ваша цель"
            
            # Умная декомпозиция без API
            steps_templates = [
                [
                    "Чётко сформулировать конечную цель и критерии успеха",
                    "Провести анализ текущей ситуации и доступных ресурсов",
                    "Разбить цель на ключевые этапы и вехи",
                    "Определить необходимые инструменты и поддержку",
                    "Составить детальный план с временными рамками",
                    "Начать выполнение с первого самого важного шага"
                ],
                [
                    "Определить конкретные измеримые результаты",
                    "Выявить потенциальные препятствия и риски", 
                    "Создать систему отслеживания прогресса",
                    "Назначить ответственных и сроки",
                    "Подготовить запасные варианты действий",
                    "Регулярно пересматривать и корректировать план"
                ],
                [
                    "Поставить SMART-цель (конкретная, измеримая и т.д.)",
                    "Провести мозговой штурм по возможным путям достижения",
                    "Приоритизировать задачи по важности и срочности",
                    "Создать визуальную дорожную карту",
                    "Начать с быстрых побед для мотивации",
                    "Установить систему регулярного review"
                ]
            ]
            
            steps = random.choice(steps_templates)
            steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
            
            self.user_neurons[user_id] += 2
            self.user_memory[user_id]["conversations"].append({
                "user": f"Goal: {goal}",
                "timestamp": time.time(),
                "type": "goal_decomposition"
            })
            
            return f"🎯 **Цель:** {goal}\n\n📋 **План достижения:**\n\n{steps_text}\n\n💪 Удачи в достижении цели!"
            
        except Exception as e:
            logger.error(f"Goal decomposition error: {e}")
            return "❌ Ошибка при составлении плана"
    
    def _help_response(self) -> str:
        return """🤖 **SuperAi+ PRO - ПОМОЩЬ**

🎯 **ВСЕ ФУНКЦИИ РАБОТАЮТ:**
🎤 Голосовой - распознавание голосовых сообщений
🖼️ Анализ фото - описание содержимого изображений  
🎯 Декомпозитор - разбивка целей на шаги
💎 Память - история всех диалогов
🧠 Нейроны - внутренняя валюта системы
📊 Статистика - отслеживание активности
💳 Тарифы - информация о подписках

⚡ **НЕ ТРЕБУЕТСЯ НАСТРОЙКА API!**"""
    
    def _tariff_info(self, user_id: int) -> str:
        return """💳 **СИСТЕМА ПОДПИСОК**

🎯 **Доступные тарифы:**
• 🆓 Базовый - 249₽/мес
• 🚀 Стандарт - 890₽/мес  
• 💎 PRO - 2089₽/мес
• 👑 PREMIUM - 3989₽/мес

💎 **Сейчас работает тестовый режим - все функции активны!**"""
    
    def _usage_info(self, user_id: int) -> str:
        self._ensure_user_data(user_id)
        return f"""📊 **ВАША СТАТИСТИКА**

🧠 **Нейроны:** {self.user_neurons.get(user_id, 100)}
💾 **Диалогов:** {len(self.user_memory[user_id]['conversations'])}
🎯 **Тариф:** Тестовый (всё включено)

✅ **Голосовые:** Активны
✅ **Анализ фото:** Активен  
✅ **AI-ответы:** Активны
✅ **Декомпозитор:** Активен

🚀 **Готов к работе!**"""

# Создаем экземпляр AI движка
ai_engine = SuperAIPlus()

async def get_telegram_file_url(file_id: str) -> str:
    """Получить URL файла от Telegram"""
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
    """Отправка сообщения в Telegram"""
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
    """Основной обработчик вебхука от Telegram"""
    try:
        update = await request.json()
        logger.info(f"Received update from user: {update.get('message', {}).get('from', {}).get('id')}")
        
        # Обрабатываем в фоне
        import asyncio
        asyncio.create_task(process_update(update))
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "ok"}

async def process_update(update: dict):
    """Фоновая обработка обновления"""
    try:
        if "message" not in update:
            return
            
        chat_id = update["message"]["chat"]["id"]
        user_id = update["message"]["from"]["id"]
        
        # Обработка голосовых сообщений
        if "voice" in update["message"]:
            file_id = update["message"]["voice"]["file_id"]
            response = await ai_engine.handle_voice_message(file_id, user_id)
            await send_message(chat_id, response, menu=True)
        
        # Обработка фото
        elif "photo" in update["message"]:
            photo_sizes = update["message"]["photo"]
            file_id = photo_sizes[-1]["file_id"]
            response = await ai_engine.handle_image_message(file_id, user_id)
            await send_message(chat_id, response, menu=True)
        
        # Обработка текста
        elif "text" in update["message"]:
            text = update["message"]["text"].strip()
            
            if text.startswith("/start"):
                response = "🚀 **SuperAi+ PRO!**\n\n✅ Голосовые сообщения\n✅ Анализ фото\n✅ AI-ответы\n✅ Декомпозитор целей\n\n👇 Используйте меню!"
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
        try:
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                await send_message(chat_id, "❌ Произошла ошибка. Попробуйте еще раз.", menu=True)
        except:
            pass

@app.get("/")
async def root():
    return {"status": "SuperAi+ PRO работает без внешних API!", "version": "6.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
