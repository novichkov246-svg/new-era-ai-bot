from fastapi import FastAPI, Request
import requests
import os
import logging

app = FastAPI()
BOT_TOKEN = "8489104550:AAFBM9lAuYjojh2DpYTOhFj5Jo-SowOJfXQ"
logger = logging.getLogger(__name__)

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        update = await request.json()
        logger.info(f"Received update: {update}")
        
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text.startswith("/start"):
                response = "🚀 **SuperAi+ АКТИВИРОВАН!**\n\n_Экосистема персонального интеллекта_\n\nДоступные команды:\n/start - начать работу\n/help - помощь\n/features - возможности"
            elif text.startswith("/help"):
                response = "🤖 **SuperAi+** - ваш персональный AI-ассистент\n\n🔮 **Основные функции:**\n• Умные текстовые запросы\n• Голосовые сообщения\n• Анализ изображений\n• Декомпозиция целей\n• Кристаллы памяти"
            elif text.startswith("/features"):
                response = "💎 **ЭКСКЛЮЗИВНЫЕ ФИЧИ SuperAi+:**\n\n• Живые кристаллы памяти\n• Нейро-импринтинг личностей\n• Эмоциональный интеллект\n• Декомпозитор целей\n• P2P Маркетплейс"
            else:
                response = f"🧠 **SuperAi+** обрабатывает ваш запрос: '{text}'\n\n_Режим полного AI скоро будет активирован..._"
            
            await send_telegram_message(chat_id, response)
            
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    
    return {"status": "ok"}

async def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        logger.error(f"Send message error: {e}")

@app.get("/")
async def root():
    return {"status": "SuperAi+ Bot работает!", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
