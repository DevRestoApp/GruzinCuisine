'''
URL документации api
https://api-ru.iiko.services

Обёртка для API iiko с функциями для всех доступных эндпоинтов.
Включает аутентификацию, обработку ошибок и документацию для каждого метода.
'''

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Импорт примеров данных для всех эндпоинтов
from data_example import *

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальные переменные
BASE_URL = "https://api-ru.iiko.services"
API_VERSION = "1.0"
API_KEY = None
ACCESS_TOKEN = None
ORGANIZATION_ID = None

# Заголовки по умолчанию
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Коды ошибок
ERROR_CODES = {
    400: "Неверный запрос",
    401: "Не авторизован",
    403: "Доступ запрещён",
    404: "Не найдено",
    429: "Слишком много запросов",
    500: "Внутренняя ошибка сервера",
    502: "Ошибка шлюза",
    503: "Сервис недоступен"
}

# ==================== ПРИМЕРЫ ДАННЫХ ДЛЯ ВСЕХ ЭНДПОИНТОВ ====================
# Для просмотра примеров данных кликните на переменную и перейдите в файл data_example.py

# Аутентификация
AUTH_EXAMPLE = AUTH_RESPONSE_EXAMPLE

# Организации
ORGANIZATIONS_EXAMPLE = ORGANIZATIONS_LIST_EXAMPLE
ORGANIZATION_BY_ID_EXAMPLE_DATA = ORGANIZATION_BY_ID_EXAMPLE

# Меню и товары
MENU_EXAMPLE_DATA = MENU_EXAMPLE
PRODUCTS_EXAMPLE = PRODUCTS_LIST_EXAMPLE
PRODUCT_BY_ID_EXAMPLE_DATA = PRODUCT_BY_ID_EXAMPLE

# Заказы
ORDER_CREATE_EXAMPLE = ORDER_CREATE_REQUEST_EXAMPLE
ORDER_RESPONSE_EXAMPLE_DATA = ORDER_RESPONSE_EXAMPLE
ORDERS_LIST_EXAMPLE_DATA = ORDERS_LIST_EXAMPLE

# Клиенты
CUSTOMER_CREATE_EXAMPLE = CUSTOMER_CREATE_REQUEST_EXAMPLE
CUSTOMER_RESPONSE_EXAMPLE_DATA = CUSTOMER_RESPONSE_EXAMPLE
CUSTOMERS_LIST_EXAMPLE_DATA = CUSTOMERS_LIST_EXAMPLE

# Склады и остатки
WAREHOUSES_EXAMPLE = WAREHOUSES_LIST_EXAMPLE
STOCK_EXAMPLE_DATA = STOCK_EXAMPLE

# Отчёты
SALES_REPORT_EXAMPLE_DATA = SALES_REPORT_EXAMPLE
PRODUCTS_REPORT_EXAMPLE_DATA = PRODUCTS_REPORT_EXAMPLE

# Доставка
DELIVERY_CREATE_EXAMPLE = DELIVERY_CREATE_REQUEST_EXAMPLE
DELIVERY_RESPONSE_EXAMPLE_DATA = DELIVERY_RESPONSE_EXAMPLE
DELIVERIES_LIST_EXAMPLE_DATA = DELIVERIES_LIST_EXAMPLE

# Резервы
RESERVE_CREATE_EXAMPLE = RESERVE_CREATE_REQUEST_EXAMPLE
RESERVE_RESPONSE_EXAMPLE_DATA = RESERVE_RESPONSE_EXAMPLE
RESERVES_LIST_EXAMPLE_DATA = RESERVES_LIST_EXAMPLE

# Столы и зоны
TABLES_EXAMPLE = TABLES_LIST_EXAMPLE
ZONES_EXAMPLE = ZONES_LIST_EXAMPLE

# Платежи
PAYMENT_CREATE_EXAMPLE = PAYMENT_CREATE_REQUEST_EXAMPLE
PAYMENT_RESPONSE_EXAMPLE_DATA = PAYMENT_RESPONSE_EXAMPLE
PAYMENTS_LIST_EXAMPLE_DATA = PAYMENTS_LIST_EXAMPLE

# Скидки и акции
DISCOUNTS_EXAMPLE = DISCOUNTS_LIST_EXAMPLE
PROMOTIONS_EXAMPLE = PROMOTIONS_LIST_EXAMPLE

# API информация
API_INFO_EXAMPLE_DATA = API_INFO_EXAMPLE

def set_api_key(api_key: str) -> None:
    """Устанавливает API ключ для аутентификации"""
    global API_KEY
    API_KEY = api_key
    logger.info("API ключ установлен")

def set_organization_id(org_id: str) -> None:
    """Устанавливает ID организации"""
    global ORGANIZATION_ID
    ORGANIZATION_ID = org_id
    logger.info(f"ID организации установлен: {org_id}")

def _make_request(method: str, endpoint: str, data: Optional[Dict] = None, 
                  params: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Выполняет HTTP запрос к API iiko
    
    Args:
        method: HTTP метод (GET, POST, PUT, DELETE)
        endpoint: Эндпоинт API
        data: Данные для отправки в теле запроса
        params: Параметры запроса
        
    Returns:
        Ответ от API в виде словаря
        
    Raises:
        requests.RequestException: При ошибке HTTP запроса
        ValueError: При неверном ответе от API
    """
    if not API_KEY:
        raise ValueError("API ключ не установлен. Используйте set_api_key()")
    
    url = f"{BASE_URL}{endpoint}"
    headers = DEFAULT_HEADERS.copy()
    headers["Authorization"] = f"Bearer {API_KEY}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, params=params)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data, params=params)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, params=params)
        else:
            raise ValueError(f"Неподдерживаемый HTTP метод: {method}")
        
        response.raise_for_status()
        
        if response.content:
            return response.json()
        return {}
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка HTTP запроса: {e}")
        if hasattr(e, 'response') and e.response is not None:
            error_msg = ERROR_CODES.get(e.response.status_code, f"Ошибка {e.response.status_code}")
            logger.error(f"Статус: {e.response.status_code}, Сообщение: {error_msg}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON: {e}")
        raise ValueError("Неверный формат ответа от API")

# ==================== АУТЕНТИФИКАЦИЯ ====================

def authenticate(login: str, password: str) -> Dict[str, Any]:
    """
    Аутентификация в API iiko
    
    Документация: https://api-ru.iiko.services/#operation/Authenticate
    
    Args:
        login: Логин пользователя
        password: Пароль пользователя
        
    Returns:
        Информация об аутентификации
    """
    endpoint = "/api/1/auth/access_token"
    data = {
        "login": login,
        "password": password
    }
    
    try:
        result = _make_request("POST", endpoint, data=data)
        global ACCESS_TOKEN
        ACCESS_TOKEN = result.get("token")
        logger.info("Аутентификация успешна")
        return result
    except Exception as e:
        logger.error(f"Ошибка аутентификации: {e}")
        raise

# ==================== ОРГАНИЗАЦИИ ====================

def get_organizations() -> List[Dict[str, Any]]:
    """
    Получение списка организаций
    
    Документация: https://api-ru.iiko.services/#operation/GetOrganizations
    
    Returns:
        Список организаций
    """
    endpoint = "/api/1/organizations"
    
    try:
        result = _make_request("GET", endpoint)
        return result.get("organizations", [])
    except Exception as e:
        logger.error(f"Ошибка получения организаций: {e}")
        raise

def get_organization_by_id(organization_id: str) -> Dict[str, Any]:
    """
    Получение информации об организации по ID
    
    Документация: https://api-ru.iiko.services/#operation/GetOrganizationById
    
    Args:
        organization_id: ID организации
        
    Returns:
        Информация об организации
    """
    endpoint = f"/api/1/organizations/{organization_id}"
    
    try:
        result = _make_request("GET", endpoint)
        return result
    except Exception as e:
        logger.error(f"Ошибка получения организации {organization_id}: {e}")
        raise

# ==================== МЕНЮ И ТОВАРЫ ====================

def get_menu(organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение меню организации
    
    Документация: https://api-ru.iiko.services/#operation/GetMenu
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Список товаров в меню
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/menu"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("items", [])
    except Exception as e:
        logger.error(f"Ошибка получения меню: {e}")
        raise

def get_products(organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка товаров
    
    Документация: https://api-ru.iiko.services/#operation/GetProducts
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Список товаров
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/products"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("products", [])
    except Exception as e:
        logger.error(f"Ошибка получения товаров: {e}")
        raise

def get_product_by_id(product_id: str, organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Получение информации о товаре по ID
    
    Документация: https://api-ru.iiko.services/#operation/GetProductById
    
    Args:
        product_id: ID товара
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Информация о товаре
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/products/{product_id}"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result
    except Exception as e:
        logger.error(f"Ошибка получения товара {product_id}: {e}")
        raise

# ==================== ЗАКАЗЫ ====================

def create_order(order_data: Dict[str, Any], organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Создание нового заказа
    
    Документация: https://api-ru.iiko.services/#operation/CreateOrder
    
    Args:
        order_data: Данные заказа
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Созданный заказ
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/orders"
    data = {**order_data, "organizationId": org_id}
    
    try:
        result = _make_request("POST", endpoint, data=data)
        logger.info(f"Заказ создан: {result.get('id')}")
        return result
    except Exception as e:
        logger.error(f"Ошибка создания заказа: {e}")
        raise

def get_order(order_id: str, organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Получение информации о заказе
    
    Документация: https://api-ru.iiko.services/#operation/GetOrder
    
    Args:
        order_id: ID заказа
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Информация о заказе
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/orders/{order_id}"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result
    except Exception as e:
        logger.error(f"Ошибка получения заказа {order_id}: {e}")
        raise

def update_order(order_id: str, order_data: Dict[str, Any], 
                organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Обновление заказа
    
    Документация: https://api-ru.iiko.services/#operation/UpdateOrder
    
    Args:
        order_id: ID заказа
        order_data: Новые данные заказа
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Обновлённый заказ
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/orders/{order_id}"
    data = {**order_data, "organizationId": org_id}
    
    try:
        result = _make_request("PUT", endpoint, data=data)
        logger.info(f"Заказ {order_id} обновлён")
        return result
    except Exception as e:
        logger.error(f"Ошибка обновления заказа {order_id}: {e}")
        raise

def delete_order(order_id: str, organization_id: Optional[str] = None) -> bool:
    """
    Удаление заказа
    
    Документация: https://api-ru.iiko.services/#operation/DeleteOrder
    
    Args:
        order_id: ID заказа
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        True если заказ успешно удалён
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/orders/{order_id}"
    params = {"organizationId": org_id}
    
    try:
        _make_request("DELETE", endpoint, params=params)
        logger.info(f"Заказ {order_id} удалён")
        return True
    except Exception as e:
        logger.error(f"Ошибка удаления заказа {order_id}: {e}")
        raise

def get_orders(organization_id: Optional[str] = None, 
               date_from: Optional[str] = None, 
               date_to: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка заказов
    
    Документация: https://api-ru.iiko.services/#operation/GetOrders
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        date_from: Дата начала периода (формат: YYYY-MM-DD)
        date_to: Дата окончания периода (формат: YYYY-MM-DD)
        
    Returns:
        Список заказов
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/orders"
    params = {"organizationId": org_id}
    
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("orders", [])
    except Exception as e:
        logger.error(f"Ошибка получения заказов: {e}")
        raise

# ==================== КЛИЕНТЫ ====================

def create_customer(customer_data: Dict[str, Any], 
                   organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Создание нового клиента
    
    Документация: https://api-ru.iiko.services/#operation/CreateCustomer
    
    Args:
        customer_data: Данные клиента
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Созданный клиент
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/customers"
    data = {**customer_data, "organizationId": org_id}
    
    try:
        result = _make_request("POST", endpoint, data=data)
        logger.info(f"Клиент создан: {result.get('id')}")
        return result
    except Exception as e:
        logger.error(f"Ошибка создания клиента: {e}")
        raise

def get_customer(customer_id: str, organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Получение информации о клиенте
    
    Документация: https://api-ru.iiko.services/#operation/GetCustomer
    
    Args:
        customer_id: ID клиента
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Информация о клиенте
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/customers/{customer_id}"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result
    except Exception as e:
        logger.error(f"Ошибка получения клиента {customer_id}: {e}")
        raise

def update_customer(customer_id: str, customer_data: Dict[str, Any], 
                   organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Обновление клиента
    
    Документация: https://api-ru.iiko.services/#operation/UpdateCustomer
    
    Args:
        customer_id: ID клиента
        customer_data: Новые данные клиента
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Обновлённый клиент
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/customers/{customer_id}"
    data = {**customer_data, "organizationId": org_id}
    
    try:
        result = _make_request("PUT", endpoint, data=data)
        logger.info(f"Клиент {customer_id} обновлён")
        return result
    except Exception as e:
        logger.error(f"Ошибка обновления клиента {customer_id}: {e}")
        raise

def get_customers(organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка клиентов
    
    Документация: https://api-ru.iiko.services/#operation/GetCustomers
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Список клиентов
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/customers"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("customers", [])
    except Exception as e:
        logger.error(f"Ошибка получения клиентов: {e}")
        raise

# ==================== СКЛАДЫ И ОСТАТКИ ====================

def get_warehouses(organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка складов
    
    Документация: https://api-ru.iiko.services/#operation/GetWarehouses
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Список складов
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/warehouses"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("warehouses", [])
    except Exception as e:
        logger.error(f"Ошибка получения складов: {e}")
        raise

def get_stock(organization_id: Optional[str] = None, 
              warehouse_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение остатков товаров
    
    Документация: https://api-ru.iiko.services/#operation/GetStock
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        warehouse_id: ID склада (если не указан, возвращаются остатки по всем складам)
        
    Returns:
        Список остатков товаров
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/stock"
    params = {"organizationId": org_id}
    
    if warehouse_id:
        params["warehouseId"] = warehouse_id
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("stock", [])
    except Exception as e:
        logger.error(f"Ошибка получения остатков: {e}")
        raise

# ==================== ОТЧЁТЫ ====================

def get_sales_report(organization_id: Optional[str] = None, 
                     date_from: Optional[str] = None, 
                     date_to: Optional[str] = None) -> Dict[str, Any]:
    """
    Получение отчёта по продажам
    
    Документация: https://api-ru.iiko.services/#operation/GetSalesReport
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        date_from: Дата начала периода (формат: YYYY-MM-DD)
        date_to: Дата окончания периода (формат: YYYY-MM-DD)
        
    Returns:
        Отчёт по продажам
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/reports/sales"
    params = {"organizationId": org_id}
    
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result
    except Exception as e:
        logger.error(f"Ошибка получения отчёта по продажам: {e}")
        raise

def get_products_report(organization_id: Optional[str] = None, 
                       date_from: Optional[str] = None, 
                       date_to: Optional[str] = None) -> Dict[str, Any]:
    """
    Получение отчёта по товарам
    
    Документация: https://api-ru.iiko.services/#operation/GetProductsReport
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        date_from: Дата начала периода (формат: YYYY-MM-DD)
        date_to: Дата окончания периода (формат: YYYY-MM-DD)
        
    Returns:
        Отчёт по товарам
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/reports/products"
    params = {"organizationId": org_id}
    
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result
    except Exception as e:
        logger.error(f"Ошибка получения отчёта по товарам: {e}")
        raise

# ==================== ДОСТАВКА ====================

def create_delivery(delivery_data: Dict[str, Any], 
                   organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Создание доставки
    
    Документация: https://api-ru.iiko.services/#operation/CreateDelivery
    
    Args:
        delivery_data: Данные доставки
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Созданная доставка
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/deliveries"
    data = {**delivery_data, "organizationId": org_id}
    
    try:
        result = _make_request("POST", endpoint, data=data)
        logger.info(f"Доставка создана: {result.get('id')}")
        return result
    except Exception as e:
        logger.error(f"Ошибка создания доставки: {e}")
        raise

def get_delivery(delivery_id: str, organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Получение информации о доставке
    
    Документация: https://api-ru.iiko.services/#operation/GetDelivery
    
    Args:
        delivery_id: ID доставки
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Информация о доставке
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/deliveries/{delivery_id}"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result
    except Exception as e:
        logger.error(f"Ошибка получения доставки {delivery_id}: {e}")
        raise

def update_delivery(delivery_id: str, delivery_data: Dict[str, Any], 
                   organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Обновление доставки
    
    Документация: https://api-ru.iiko.services/#operation/UpdateDelivery
    
    Args:
        delivery_id: ID доставки
        delivery_data: Новые данные доставки
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Обновлённая доставка
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/deliveries/{delivery_id}"
    data = {**delivery_data, "organizationId": org_id}
    
    try:
        result = _make_request("PUT", endpoint, data=data)
        logger.info(f"Доставка {delivery_id} обновлена")
        return result
    except Exception as e:
        logger.error(f"Ошибка обновления доставки {delivery_id}: {e}")
        raise

def get_deliveries(organization_id: Optional[str] = None, 
                   date_from: Optional[str] = None, 
                   date_to: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка доставок
    
    Документация: https://api-ru.iiko.services/#operation/GetDeliveries
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        date_from: Дата начала периода (формат: YYYY-MM-DD)
        date_to: Дата окончания периода (формат: YYYY-MM-DD)
        
    Returns:
        Список доставок
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/deliveries"
    params = {"organizationId": org_id}
    
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("deliveries", [])
    except Exception as e:
        logger.error(f"Ошибка получения доставок: {e}")
        raise

# ==================== РЕЗЕРВЫ ====================

def create_reserve(reserve_data: Dict[str, Any], 
                  organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Создание резерва стола
    
    Документация: https://api-ru.iiko.services/#operation/CreateReserve
    
    Args:
        reserve_data: Данные резерва
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Созданный резерв
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/reserves"
    data = {**reserve_data, "organizationId": org_id}
    
    try:
        result = _make_request("POST", endpoint, data=data)
        logger.info(f"Резерв создан: {result.get('id')}")
        return result
    except Exception as e:
        logger.error(f"Ошибка создания резерва: {e}")
        raise

def get_reserve(reserve_id: str, organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Получение информации о резерве
    
    Документация: https://api-ru.iiko.services/#operation/GetReserve
    
    Args:
        reserve_id: ID резерва
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Информация о резерве
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/reserves/{reserve_id}"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result
    except Exception as e:
        logger.error(f"Ошибка получения резерва {reserve_id}: {e}")
        raise

def update_reserve(reserve_id: str, reserve_data: Dict[str, Any], 
                  organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Обновление резерва
    
    Документация: https://api-ru.iiko.services/#operation/UpdateReserve
    
    Args:
        reserve_id: ID резерва
        reserve_data: Новые данные резерва
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Обновлённый резерв
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/reserves/{reserve_id}"
    data = {**reserve_data, "organizationId": org_id}
    
    try:
        result = _make_request("PUT", endpoint, data=data)
        logger.info(f"Резерв {reserve_id} обновлён")
        return result
    except Exception as e:
        logger.error(f"Ошибка обновления резерва {reserve_id}: {e}")
        raise

def cancel_reserve(reserve_id: str, organization_id: Optional[str] = None) -> bool:
    """
    Отмена резерва
    
    Документация: https://api-ru.iiko.services/#operation/CancelReserve
    
    Args:
        reserve_id: ID резерва
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        True если резерв успешно отменён
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/reserves/{reserve_id}/cancel"
    params = {"organizationId": org_id}
    
    try:
        _make_request("POST", endpoint, params=params)
        logger.info(f"Резерв {reserve_id} отменён")
        return True
    except Exception as e:
        logger.error(f"Ошибка отмены резерва {reserve_id}: {e}")
        raise

def get_reserves(organization_id: Optional[str] = None, 
                 date_from: Optional[str] = None, 
                 date_to: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка резервов
    
    Документация: https://api-ru.iiko.services/#operation/GetReserves
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        date_from: Дата начала периода (формат: YYYY-MM-DD)
        date_to: Дата окончания периода (формат: YYYY-MM-DD)
        
    Returns:
        Список резервов
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/reserves"
    params = {"organizationId": org_id}
    
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("reserves", [])
    except Exception as e:
        logger.error(f"Ошибка получения резервов: {e}")
        raise

# ==================== СТОЛЫ И ЗОНЫ ====================

def get_tables(organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка столов
    
    Документация: https://api-ru.iiko.services/#operation/GetTables
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Список столов
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/tables"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("tables", [])
    except Exception as e:
        logger.error(f"Ошибка получения столов: {e}")
        raise

def get_zones(organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка зон
    
    Документация: https://api-ru.iiko.services/#operation/GetZones
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Список зон
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/zones"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("zones", [])
    except Exception as e:
        logger.error(f"Ошибка получения зон: {e}")
        raise

# ==================== ПЛАТЕЖИ ====================

def create_payment(payment_data: Dict[str, Any], 
                  organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Создание платежа
    
    Документация: https://api-ru.iiko.services/#operation/CreatePayment
    
    Args:
        payment_data: Данные платежа
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Созданный платёж
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/payments"
    data = {**payment_data, "organizationId": org_id}
    
    try:
        result = _make_request("POST", endpoint, data=data)
        logger.info(f"Платёж создан: {result.get('id')}")
        return result
    except Exception as e:
        logger.error(f"Ошибка создания платежа: {e}")
        raise

def get_payment(payment_id: str, organization_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Получение информации о платеже
    
    Документация: https://api-ru.iiko.services/#operation/GetPayment
    
    Args:
        payment_id: ID платежа
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Информация о платеже
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = f"/api/1/payments/{payment_id}"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result
    except Exception as e:
        logger.error(f"Ошибка получения платежа {payment_id}: {e}")
        raise

def get_payments(organization_id: Optional[str] = None, 
                 date_from: Optional[str] = None, 
                 date_to: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка платежей
    
    Документация: https://api-ru.iiko.services/#operation/GetPayments
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        date_from: Дата начала периода (формат: YYYY-MM-DD)
        date_to: Дата окончания периода (формат: YYYY-MM-DD)
        
    Returns:
        Список платежей
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/payments"
    params = {"organizationId": org_id}
    
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("payments", [])
    except Exception as e:
        logger.error(f"Ошибка получения платежей: {e}")
        raise

# ==================== СКИДКИ И АКЦИИ ====================

def get_discounts(organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка скидок
    
    Документация: https://api-ru.iiko.services/#operation/GetDiscounts
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Список скидок
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/discounts"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("discounts", [])
    except Exception as e:
        logger.error(f"Ошибка получения скидок: {e}")
        raise

def get_promotions(organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Получение списка акций
    
    Документация: https://api-ru.iiko.services/#operation/GetPromotions
    
    Args:
        organization_id: ID организации (если не указан, используется глобальный)
        
    Returns:
        Список акций
    """
    org_id = organization_id or ORGANIZATION_ID
    if not org_id:
        raise ValueError("ID организации не указан")
    
    endpoint = "/api/1/promotions"
    params = {"organizationId": org_id}
    
    try:
        result = _make_request("GET", endpoint, params=params)
        return result.get("promotions", [])
    except Exception as e:
        logger.error(f"Ошибка получения акций: {e}")
        raise

# ==================== УТИЛИТЫ ====================

def get_api_info() -> Dict[str, Any]:
    """
    Получение информации об API
    
    Документация: https://api-ru.iiko.services/#operation/GetApiInfo
    
    Returns:
        Информация об API
    """
    endpoint = "/api/1/info"
    
    try:
        result = _make_request("GET", endpoint)
        return result
    except Exception as e:
        logger.error(f"Ошибка получения информации об API: {e}")
        raise

def check_connection() -> bool:
    """
    Проверка соединения с API
    
    Returns:
        True если соединение установлено
    """
    try:
        get_api_info()
        logger.info("Соединение с API установлено")
        return True
    except Exception as e:
        logger.error(f"Ошибка соединения с API: {e}")
        return False

def get_error_description(error_code: int) -> str:
    """
    Получение описания ошибки по коду
    
    Args:
        error_code: Код ошибки
        
    Returns:
        Описание ошибки
    """
    return ERROR_CODES.get(error_code, f"Неизвестная ошибка: {error_code}")

# ==================== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ====================

def example_usage():
    """
    Пример использования API обёртки
    """
    print("=== Пример использования iiko API обёртки ===")
    
    # Установка API ключа
    set_api_key("your_api_key_here")
    
    # Установка ID организации
    set_organization_id("your_organization_id_here")
    
    # Проверка соединения
    if check_connection():
        print("✓ Соединение установлено")
        
        # Получение списка организаций
        try:
            orgs = get_organizations()
            print(f"✓ Найдено организаций: {len(orgs)}")
        except Exception as e:
            print(f"✗ Ошибка получения организаций: {e}")
        
        # Получение меню
        try:
            menu = get_menu()
            print(f"✓ Получено товаров в меню: {len(menu)}")
        except Exception as e:
            print(f"✗ Ошибка получения меню: {e}")
    else:
        print("✗ Соединение не установлено")

if __name__ == "__main__":
    example_usage()