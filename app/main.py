from fastapi import FastAPI, Request
import requests
import logging
import time
import threading
import random

app = FastAPI()
BOT_TOKEN = "8489104550:AAFBM9lAuYjojh2DpYTOhFj5Jo-SowOJfXQ"
logger = logging.getLogger(__name__)

# Авто-пингер
def keep_alive():
    while True:
        try:
            requests.get("https://new-era-ai-bot.onrender.com", timeout=10)
        except:
            pass
        time.sleep(300)  # 5 минут

threading.Thread(target=keep_alive, daemon=True).start()

class SmartAI:
    RESPONSES = {
        "привет": "🚀 Привет! Я SuperAi+ - твой умный помощник! Спрашивай что угодно!",
        "как дела": "💎 Отлично! Работаю на максимальной скорости! А у тебя?",
        "кто ты": "🤖 Я SuperAi+ - продвинутый AI-помощник на базе DeepSeek!",
        "что ты умеешь": "🔮 **Мои способности:**\n• Отвечать на вопросы\n• Помогать с учебой\n• Создавать планы\n• Анализировать задачи\n• Работать 24/7",
        "сколько тебе лет": "🤖 Я цифровой помощник - мой код постоянно обновляется! Можно сказать, я всегда современный!",
        "стой": "🛑 Остановился! Что нужно? Готов помочь!",
        "что делаешь": "💎 Анализирую твои запросы и готовлю точные ответы! Чем могу помочь?",
    }

    @staticmethod
    def get_response(message: str) -> str:
        message_lower = message.lower()
        
        # Точные совпадения
        for question, answer in SmartAI.RESPONSES.items():
            if question in message_lower:
                return answer
        
        # Умные ответы по типам
        if any(word in message_lower for word in ['помоги', 'сделай', 'реши']):
            return SmartAI.help_response(message)
        elif any(word in message_lower for word in ['сколько', 'когда', 'где', 'почему']):
            return SmartAI.question_response(message)
        elif any(word in message_lower for word in ['задача', 'план', 'проект']):
            return SmartAI.plan_response(message)
        else:
            return SmartAI.general_response(message)

    @staticmethod
    def help_response(task: str) -> str:
        return f"🎯 **Помогу с этим!**\n\n**Задача:** {task}\n\n💡 **Что нужно уточнить:**\n• Конкретная цель\n• Предмет/направление\n• Сроки\n• Текущий прогресс\n\nОпиши подробнее - составлю план!"

    @staticmethod
    def question_response(question: str) -> str:
        return f"🤔 **Интересный вопрос!**\n\n_{question}_\n\n💡 Давайте разберем его детально! Что именно вас интересует больше всего?"

    @staticmethod
    def plan_response(task: str) -> str:
        return f"📋 **План для задачи:**\n\n**{task}**\n\n✅ Шаг 1: Анализ и постановка цели\n✅ Шаг 2: Разработка стратегии\n✅ Шаг 3: Реализация\n✅ Шаг 4: Проверка результатов\n\n🚀 _Готов детализировать каждый шаг!_"

    @staticmethod
    def general_response(message: str) -> str:
        responses = [
            f"🔮 **Понимаю ваш запрос!**\n\n_{message}_\n\n💡 Могу помочь с анализом, решением задач или созданием плана!",
            f"🚀 **Интересно!**\n\n**Запрос:** {message}\n\n💎 Давайте разберем это подробнее! Что именно вас интересует?",
            f"🎯 **Анализирую...**\n\n_{message}_\n\n💡 Готов предложить решение или помощь! Уточните задачу?"
        ]
        return random.choice(responses)

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        update = await request.json()
        
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "").strip()
            
            if text.startswith("/start"):
                response = "🚀 **SuperAi+ УМНЫЙ РЕЖИМ!**\n\n💎 Теперь я понимаю контекст и даю точные ответы!\n\n**Просто спроси о чем угодно!**"
            elif text.startswith("/help"):
                response = "🤖 **Помощь:**\n• Задавай вопросы\n• Проси помощи с задачами\n• Спрашивай совета\n• Уточняй если что-то непонятно\n\n💎 Я пойму и помогу!"
            else:
                response = SmartAI.get_response(text)
            
            await send_telegram_message(chat_id, response)
            
    except Exception as e:
        logger.error(f"Error: {e}")
    
    return {"status": "ok"}

async def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

@app.get("/")
async def root():
    return {"status": "SuperAi+ SMART работает!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
