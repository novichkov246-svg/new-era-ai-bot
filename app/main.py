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
                response = "🔮 NEW ERA AI активирован!\n\nДоступные команды:\n/start - начать работу\n/help - помощь"
            elif text.startswith("/help"):
                response = "🤖 Я ваш персональный AI-ассистент\n\nФункции:\n• Текстовые запросы\n• Голосовые сообщения\n• Анализ изображений\n• Декомпозиция целей"
            else:
                response = f"🧠 Ваш запрос: '{text}'\n\n(Режим AI скоро будет активирован)"
            
            await send_telegram_message(chat_id, response)
            
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    
    return {"status": "ok"}

async def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        logger.error(f"Send message error: {e}")

@app.get("/")
async def root():
    return {"status": "NEW ERA AI Bot работает!", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
