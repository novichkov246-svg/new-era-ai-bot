import time
from typing import Dict
from enum import Enum

class Tariff(Enum):
    BASIC = "basic"
    STANDARD = "standard"  
    PRO = "pro"
    PREMIUM = "premium"

class SubscriptionManager:
    def __init__(self):
        self.tariffs = {
            Tariff.BASIC: {
                "name": "Базовый",
                "price": 249,
                "limits": {
                    "ai_requests_per_day": 20,
                    "voice_messages_per_day": 5,
                    "image_analysis_per_day": 3,
                    "memory_crystals": 10,
                    "neurons_earning_multiplier": 1.0
                },
                "features": ["Базовый AI", "Текстовая память", "Простой декомпозитор"]
            },
            Tariff.STANDARD: {
                "name": "Стандарт", 
                "price": 890,
                "limits": {
                    "ai_requests_per_day": 100,
                    "voice_messages_per_day": 20,
                    "image_analysis_per_day": 15,
                    "memory_crystals": 50,
                    "neurons_earning_multiplier": 1.5
                },
                "features": ["Продвинутый AI", "Расширенная память", "Декомпозитор целей", "Голосовые сообщения"]
            },
            Tariff.PRO: {
                "name": "PRO",
                "price": 2089,
                "limits": {
                    "ai_requests_per_day": 500,
                    "voice_messages_per_day": 100,
                    "image_analysis_per_day": 50,
                    "memory_crystals": 200,
                    "neurons_earning_multiplier": 2.0
                },
                "features": ["PRO AI", "Неограниченная память", "Продвинутый декомпозитор", "Приоритетная обработка"]
            },
            Tariff.PREMIUM: {
                "name": "PREMIUM",
                "price": 3989,
                "limits": {
                    "ai_requests_per_day": 1000,
                    "voice_messages_per_day": 300,
                    "image_analysis_per_day": 100,
                    "memory_crystals": 500,
                    "neurons_earning_multiplier": 3.0
                },
                "features": ["PREMIUM AI", "Все функции", "Персональная поддержка", "Ранний доступ к фичам"]
            }
        }
        
        self.user_subscriptions = {}
        self.user_usage = {}
    
    def _reset_user_usage(self, user_id: int):
        self.user_usage[user_id] = {
            "ai_requests_today": 0,
            "voice_messages_today": 0, 
            "image_analysis_today": 0,
            "last_reset": time.time()
        }
    
    def get_user_tariff(self, user_id: int) -> Tariff:
        return self.user_subscriptions.get(user_id, {}).get("tariff", Tariff.BASIC)
    
    def can_use_feature(self, user_id: int, feature: str) -> bool:
        if user_id not in self.user_usage:
            self._reset_user_usage(user_id)
            
        tariff = self.get_user_tariff(user_id)
        limits = self.tariffs[tariff]["limits"]
        
        if feature == "ai_request":
            return self.user_usage[user_id]["ai_requests_today"] < limits["ai_requests_per_day"]
        elif feature == "voice_message":
            return self.user_usage[user_id]["voice_messages_today"] < limits["voice_messages_per_day"]
        elif feature == "image_analysis":
            return self.user_usage[user_id]["image_analysis_today"] < limits["image_analysis_per_day"]
        return True
    
    def record_usage(self, user_id: int, feature: str):
        if user_id not in self.user_usage:
            self._reset_user_usage(user_id)
            
        if feature == "ai_request":
            self.user_usage[user_id]["ai_requests_today"] += 1
        elif feature == "voice_message":
            self.user_usage[user_id]["voice_messages_today"] += 1
        elif feature == "image_analysis":
            self.user_usage[user_id]["image_analysis_today"] += 1
    
    def get_usage_stats(self, user_id: int) -> Dict:
        if user_id not in self.user_usage:
            self._reset_user_usage(user_id)
            
        tariff = self.get_user_tariff(user_id)
        limits = self.tariffs[tariff]["limits"]
        
        return {
            "tariff": self.tariffs[tariff]["name"],
            "usage": {
                "ai_requests": f"{self.user_usage[user_id]['ai_requests_today']}/{limits['ai_requests_per_day']}",
                "voice_messages": f"{self.user_usage[user_id]['voice_messages_today']}/{limits['voice_messages_per_day']}",
                "image_analysis": f"{self.user_usage[user_id]['image_analysis_today']}/{limits['image_analysis_per_day']}"
            }
        }

subscription_manager = SubscriptionManager()
