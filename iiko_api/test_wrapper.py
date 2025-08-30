#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый файл для проверки работы iiko API обёртки
"""

import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iiko_api_wrapper import (
    set_api_key, 
    set_organization_id, 
    check_connection,
    get_organizations,
    get_api_info,
    get_error_description
)

def test_basic_functionality():
    """Тестирование базовой функциональности"""
    print("=== Тестирование базовой функциональности ===")
    
    # Тест установки API ключа
    try:
        set_api_key("test_key_123")
        print("✓ API ключ установлен")
    except Exception as e:
        print(f"✗ Ошибка установки API ключа: {e}")
    
    # Тест установки ID организации
    try:
        set_organization_id("test_org_123")
        print("✓ ID организации установлен")
    except Exception as e:
        print(f"✗ Ошибка установки ID организации: {e}")
    
    # Тест получения описания ошибок
    try:
        error_400 = get_error_description(400)
        error_404 = get_error_description(404)
        print(f"✓ Описания ошибок получены: 400 - {error_400}, 404 - {error_404}")
    except Exception as e:
        print(f"✗ Ошибка получения описаний ошибок: {e}")

def test_api_connection():
    """Тестирование соединения с API"""
    print("\n=== Тестирование соединения с API ===")
    
    try:
        # Проверка соединения
        if check_connection():
            print("✓ Соединение с API установлено")
            
            # Получение информации об API
            try:
                api_info = get_api_info()
                print(f"✓ Информация об API получена: {api_info}")
            except Exception as e:
                print(f"✗ Ошибка получения информации об API: {e}")
                
        else:
            print("✗ Соединение с API не установлено")
            
    except Exception as e:
        print(f"✗ Ошибка проверки соединения: {e}")

def test_organizations():
    """Тестирование работы с организациями"""
    print("\n=== Тестирование работы с организациями ===")
    
    try:
        # Получение списка организаций
        organizations = get_organizations()
        print(f"✓ Получено организаций: {len(organizations)}")
        
        if organizations:
            # Вывод первой организации
            first_org = organizations[0]
            print(f"  Первая организация: {first_org.get('name', 'Без названия')} (ID: {first_org.get('id', 'N/A')})")
            
    except Exception as e:
        print(f"✗ Ошибка получения организаций: {e}")

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования iiko API обёртки")
    print("=" * 50)
    
    # Базовые тесты
    test_basic_functionality()
    
    # Тесты API (требуют валидный API ключ)
    print("\n⚠️  Для тестирования API функций требуется валидный API ключ")
    print("   Установите API_KEY в переменных окружения или в коде")
    
    # Раскомментируйте следующие строки после установки API ключа:
    # test_api_connection()
    # test_organizations()
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено")

if __name__ == "__main__":
    main()
