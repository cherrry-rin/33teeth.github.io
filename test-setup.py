#!/usr/bin/env python3
"""
Тестовый скрипт для проверки и настройки системы "33 Зуб"
"""

import requests
import json
import time
import sys

# Конфигурация
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_backend_connection():
    """Тестирование подключения к backend серверу"""
    print("🔍 Тестирование подключения к backend серверу...")
    
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend сервер доступен")
            return True
        else:
            print(f"❌ Backend сервер вернул статус {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к backend серверу")
        print("   Убедитесь, что сервер запущен на http://localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Таймаут подключения к backend серверу")
        return False

def test_feedback_api():
    """Тестирование API обратной связи"""
    print("\n📝 Тестирование API обратной связи...")
    
    # Тест создания сообщения
    feedback_data = {
        "name": "Тестовый Пользователь",
        "email": "test@example.com",
        "phone": "+79991234567",
        "subject": "Тестовое сообщение",
        "message": "Это тестовое сообщение для проверки API"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/feedback/",
            json=feedback_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            feedback_id = result.get("id")
            print(f"✅ Сообщение успешно создано (ID: {feedback_id})")
            
            # Тест получения сообщения
            response = requests.get(f"{API_BASE}/feedback/{feedback_id}", timeout=10)
            if response.status_code == 200:
                print("✅ Получение сообщения по ID работает")
            else:
                print(f"❌ Ошибка получения сообщения: {response.status_code}")
            
            # Тест получения всех сообщений
            response = requests.get(f"{API_BASE}/feedback/", timeout=10)
            if response.status_code == 200:
                feedbacks = response.json()
                print(f"✅ Получение всех сообщений работает (найдено: {len(feedbacks)})")
            else:
                print(f"❌ Ошибка получения всех сообщений: {response.status_code}")
            
            return True
        else:
            print(f"❌ Ошибка создания сообщения: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании API обратной связи: {e}")
        return False

def test_subscriber_api():
    """Тестирование API подписчиков"""
    print("\n📧 Тестирование API подписчиков...")
    
    test_email = "test_subscriber@example.com"
    
    try:
        # Тест подписки
        response = requests.post(
            f"{API_BASE}/subscriber/",
            json={"email": test_email},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Подписка на email {test_email} прошла успешно")
            
            # Тест проверки подписки
            response = requests.get(f"{API_BASE}/subscriber/{test_email}", timeout=10)
            if response.status_code == 200:
                print("✅ Проверка подписки работает")
            else:
                print(f"❌ Ошибка проверки подписки: {response.status_code}")
            
            # Тест отписки
            response = requests.delete(f"{API_BASE}/subscriber/{test_email}", timeout=10)
            if response.status_code == 200:
                print("✅ Отписка работает")
            else:
                print(f"❌ Ошибка отписки: {response.status_code}")
            
            return True
        else:
            print(f"❌ Ошибка подписки: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании API подписчиков: {e}")
        return False

def test_cors():
    """Тестирование CORS настроек"""
    print("\n🌐 Тестирование CORS настроек...")
    
    try:
        # Проверка OPTIONS запроса
        response = requests.options(f"{API_BASE}/feedback/", timeout=10)
        if response.status_code == 200:
            print("✅ CORS настройки работают (OPTIONS запрос успешен)")
            return True
        else:
            print(f"❌ CORS настройки могут быть проблемными (OPTIONS: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Ошибка при тестировании CORS: {e}")
        return False

def check_frontend():
    """Проверка доступности frontend"""
    print("\n🌐 Проверка доступности frontend...")
    
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend доступен на http://localhost:5173")
            return True
        else:
            print(f"❌ Frontend недоступен (статус: {response.status_code})")
            return False
    except:
        print("❌ Frontend недоступен")
        print("   Убедитесь, что frontend запущен на http://localhost:5173")
        return False

def check_admin():
    """Проверка доступности админки"""
    print("\n🔒 Проверка доступности админки...")
    
    try:
        response = requests.get("http://localhost:3001", timeout=5)
        if response.status_code == 200:
            print("✅ Админка доступна на http://localhost:3001")
            return True
        else:
            print(f"❌ Админка недоступна (статус: {response.status_code})")
            return False
    except:
        print("❌ Админка недоступна")
        print("   Убедитесь, что админка запущена на http://localhost:3001")
        return False

def print_summary(results):
    """Вывод итогов тестирования"""
    print("\n" + "="*50)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ")
    print("="*50)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test_name, result in results.items():
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"{test_name:<30} {status}")
    
    print("-"*50)
    print(f"Всего тестов: {total_tests}")
    print(f"Пройдено: {passed_tests}")
    print(f"Провалено: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        print("\n🎉 Все тесты пройдены! Система готова к использованию.")
        return True
    else:
        print(f"\n⚠️  Пройдено только {passed_tests}/{total_tests} тестов.")
        print("   Проверьте настройки и перезапустите тестирование.")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования системы '33 Зуб'")
    print("="*50)
    
    results = {}
    
    # Тесты backend
    results["Backend Connection"] = test_backend_connection()
    
    if results["Backend Connection"]:
        results["Feedback API"] = test_feedback_api()
        results["Subscriber API"] = test_subscriber_api()
        results["CORS Settings"] = test_cors()
    
    # Тесты frontend
    results["Frontend"] = check_frontend()
    results["Admin Panel"] = check_admin()
    
    # Итоги
    success = print_summary(results)
    
    if not success:
        print("\n💡 Рекомендации:")
        print("1. Убедитесь, что все серверы запущены")
        print("2. Проверьте настройки базы данных")
        print("3. Проверьте CORS настройки в backend")
        print("4. Перезапустите тестирование")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)