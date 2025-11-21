import time
from typing import Dict, List
from enum import Enum

class Tariff(Enum):
    BASIC = "basic"      # 249₽
    STANDARD = "standard" # 890₽  
    PRO = "pro"          # 2089₽
    PREMIUM = "premium"  # 3989₽

class SubscriptionManager:
    def __init__(self):
        self.tariffs = {
            Tariff.BASIC: {
                "name": "Базовый",
                "price": 249,
                "limits": {
                    "ai_requests_per_day": 50,
                    "voice_messages_per_day": 10,
                    "image_analysis_per_day": 5,
                    "memory_crystals": 10,
                    "max_goal_steps": 5,
                    "neurons_earning_multiplier": 1.0
                },
                "features": ["Базовый AI", "Текстовая память", "Простой декомпозитор"]
            },
            Tariff.STANDARD: {
                "name": "Стандарт", 
                "price": 890,
                "limits": {
                    "ai_requests_per_day": 200,
                    "voice_messages_per_day": 30,
                    "image_analysis_per_day": 20,
                    "memory_crystals": 50,
                    "max_goal_steps": 10,
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
                    "max_goal_steps": 25,
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
                    "max_goal_steps": 50,
                    "neurons_earning_multiplier": 3.0
                },
                "features": ["PREMIUM AI", "Все функции", "Персональная поддержка", "Ранний доступ к фичам"]
            }
        }
        
        self.user_subscriptions: Dict[int, Dict] = {}
        self.user_usage: Dict[int, Dict] = {}
    
    def get_user_tariff(self, user_id: int) -> Tariff:
        """Получить тариф пользователя"""
        return self.user_subscriptions.get(user_id, {}).get("tariff", Tariff.BASIC)
    
    def set_user_tariff(self, user_id: int, tariff: Tariff, duration_days: int = 30):
        """Установить тариф пользователю"""
        self.user_subscriptions[user_id] = {
            "tariff": tariff,
            "start_date": time.time(),
            "end_date": time.time() + (duration_days * 24 * 3600),
            "is_active": True
        }
        
        # Сбрасываем статистику использования
        self._reset_user_usage(user_id)
    
    def can_use_feature(self, user_id: int, feature: str) -> bool:
        """Проверить может ли пользователь использовать функцию"""
        if user_id not in self.user_usage:
            self._reset_user_usage(user_id)
            
        tariff = self.get_user_tariff(user_id)
        limits = self.tariffs[tariff]["limits"]
        
        # Проверяем дневные лимиты
        if feature == "ai_request":
            return self.user_usage[user_id]["ai_requests_today"] < limits["ai_requests_per_day"]
        elif feature == "voice_message":
            return self.user_usage[user_id]["voice_messages_today"] < limits["voice_messages_per_day"]
        elif feature == "image_analysis":
            return self.user_usage[user_id]["image_analysis_today"] < limits["image_analysis_per_day"]
        elif feature == "memory_crystal":
            return len(self.user_usage[user_id]["memory_crystals"]) < limits["memory_crystals"]
        elif feature == "goal_steps":
            return True  # Проверяется отдельно при создании цели
            
        return True
    
    def record_usage(self, user_id: int, feature: str, details: Dict = None):
        """Записать использование функции"""
        if user_id not in self.user_usage:
            self._reset_user_usage(user_id)
            
        if feature == "ai_request":
            self.user_usage[user_id]["ai_requests_today"] += 1
        elif feature == "voice_message":
            self.user_usage[user_id]["voice_messages_today"] += 1
        elif feature == "image_analysis":
            self.user_usage[user_id]["image_analysis_today"] += 1
        elif feature == "memory_crystal":
            if details and "crystal_id" in details:
                self.user_usage[user_id]["memory_crystals"].append(details["crystal_id"])
    
    def get_usage_stats(self, user_id: int) -> Dict:
        """Получить статистику использования"""
        if user_id not in self.user_usage:
            self._reset_user_usage(user_id)
            
        tariff = self.get_user_tariff(user_id)
        limits = self.tariffs[tariff]["limits"]
        
        return {
            "tariff": self.tariffs[tariff]["name"],
            "usage": {
                "ai_requests": f"{self.user_usage[user_id]['ai_requests_today']}/{limits['ai_requests_per_day']}",
                "voice_messages": f"{self.user_usage[user_id]['voice_messages_today']}/{limits['voice_messages_per_day']}",
                "image_analysis": f"{self.user_usage[user_id]['image_analysis_today']}/{limits['image_analysis_per_day']}",
                "memory_crystals": f"{len(self.user_usage[user_id]['memory_crystals'])}/{limits['memory_crystals']}"
            },
            "remaining_days": self._get_remaining_days(user_id)
        }
    
    def _reset_user_usage(self, user_id: int):
        """Сбросить дневную статистику"""
        self.user_usage[user_id] = {
            "ai_requests_today": 0,
            "voice_messages_today": 0, 
            "image_analysis_today": 0,
            "memory_crystals": [],
            "last_reset": time.time()
        }
    
    def _get_remaining_days(self, user_id: int) -> int:
        """Получить оставшиеся дни подписки"""
        if user_id not in self.user_subscriptions:
            return 0
            
        sub = self.user_subscriptions[user_id]
        if not sub["is_active"]:
            return 0
            
        remaining_seconds = sub["end_date"] - time.time()
        return max(0, int(remaining_seconds / (24 * 3600)))
    
    def get_tariff_info(self, tariff: Tariff) -> Dict:
        """Получить информацию о тарифе"""
        return self.tariffs[tariff]

# Глобальный экземпляр
subscription_manager = SubscriptionManager()
