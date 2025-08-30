"""
ООП версия обёртки для API iiko
Документация: https://api-ru.iiko.services
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from abc import ABC, abstractmethod

# Импорт примеров данных
from data_example import *

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IikoApiException(Exception):
    """Базовый класс для исключений API iiko"""
    pass

class AuthenticationError(IikoApiException):
    """Ошибка аутентификации"""
    pass

class ValidationError(IikoApiException):
    """Ошибка валидации данных"""
    pass

class ApiRequestError(IikoApiException):
    """Ошибка HTTP запроса"""
    pass

class BaseApiClient(ABC):
    """Базовый класс для API клиентов"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """Выполняет HTTP запрос"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, params=params)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, params=params)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, params=params)
            else:
                raise ValidationError(f"Неподдерживаемый HTTP метод: {method}")
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка HTTP запроса: {e}")
            raise ApiRequestError(f"Ошибка HTTP запроса: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            raise ValidationError("Неверный формат ответа от API")

class IikoAuthClient(BaseApiClient):
    """Клиент для аутентификации"""
    
    def authenticate(self, login: str, password: str) -> Dict[str, Any]:
        """
        Аутентификация пользователя
        
        Документация: https://api-ru.iiko.services/#operation/Authenticate
        
        Args:
            login: Логин пользователя
            password: Пароль пользователя
            
        Returns:
            Информация об аутентификации
            
        Raises:
            AuthenticationError: При ошибке аутентификации
        """
        endpoint = "/api/1/auth/access_token"
        data = {
            "login": login,
            "password": password
        }
        
        try:
            result = self._make_request("POST", endpoint, data=data)
            logger.info("Аутентификация успешна")
            return result
        except Exception as e:
            logger.error(f"Ошибка аутентификации: {e}")
            raise AuthenticationError(f"Ошибка аутентификации: {e}")

class IikoOrganizationsClient(BaseApiClient):
    """Клиент для работы с организациями"""
    
    def get_organizations(self) -> List[Dict[str, Any]]:
        """
        Получение списка организаций
        
        Документация: https://api-ru.iiko.services/#operation/GetOrganizations
        
        Returns:
            Список организаций
        """
        endpoint = "/api/1/organizations"
        
        try:
            result = self._make_request("GET", endpoint)
            return result.get("organizations", [])
        except Exception as e:
            logger.error(f"Ошибка получения организаций: {e}")
            raise
    
    def get_organization_by_id(self, organization_id: str) -> Dict[str, Any]:
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
            result = self._make_request("GET", endpoint)
            return result
        except Exception as e:
            logger.error(f"Ошибка получения организации {organization_id}: {e}")
            raise

class IikoMenuClient(BaseApiClient):
    """Клиент для работы с меню и товарами"""
    
    def __init__(self, base_url: str, api_key: str, organization_id: str):
        super().__init__(base_url, api_key)
        self.organization_id = organization_id
    
    def get_menu(self) -> List[Dict[str, Any]]:
        """
        Получение меню организации
        
        Документация: https://api-ru.iiko.services/#operation/GetMenu
        
        Returns:
            Список товаров в меню
        """
        endpoint = "/api/1/menu"
        params = {"organizationId": self.organization_id}
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result.get("items", [])
        except Exception as e:
            logger.error(f"Ошибка получения меню: {e}")
            raise
    
    def get_products(self) -> List[Dict[str, Any]]:
        """
        Получение списка товаров
        
        Документация: https://api-ru.iiko.services/#operation/GetProducts
        
        Returns:
            Список товаров
        """
        endpoint = "/api/1/products"
        params = {"organizationId": self.organization_id}
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result.get("products", [])
        except Exception as e:
            logger.error(f"Ошибка получения товаров: {e}")
            raise
    
    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """
        Получение информации о товаре по ID
        
        Документация: https://api-ru.iiko.services/#operation/GetProductById
        
        Args:
            product_id: ID товара
            
        Returns:
            Информация о товаре
        """
        endpoint = f"/api/1/products/{product_id}"
        params = {"organizationId": self.organization_id}
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result
        except Exception as e:
            logger.error(f"Ошибка получения товара {product_id}: {e}")
            raise

class IikoOrdersClient(BaseApiClient):
    """Клиент для работы с заказами"""
    
    def __init__(self, base_url: str, api_key: str, organization_id: str):
        super().__init__(base_url, api_key)
        self.organization_id = organization_id
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создание нового заказа
        
        Документация: https://api-ru.iiko.services/#operation/CreateOrder
        
        Args:
            order_data: Данные заказа
            
        Returns:
            Созданный заказ
        """
        endpoint = "/api/1/orders"
        data = {**order_data, "organizationId": self.organization_id}
        
        try:
            result = self._make_request("POST", endpoint, data=data)
            logger.info(f"Заказ создан: {result.get('id')}")
            return result
        except Exception as e:
            logger.error(f"Ошибка создания заказа: {e}")
            raise
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        """
        Получение информации о заказе
        
        Документация: https://api-ru.iiko.services/#operation/GetOrder
        
        Args:
            order_id: ID заказа
            
        Returns:
            Информация о заказе
        """
        endpoint = f"/api/1/orders/{order_id}"
        params = {"organizationId": self.organization_id}
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result
        except Exception as e:
            logger.error(f"Ошибка получения заказа {order_id}: {e}")
            raise
    
    def update_order(self, order_id: str, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обновление заказа
        
        Документация: https://api-ru.iiko.services/#operation/UpdateOrder
        
        Args:
            order_id: ID заказа
            order_data: Новые данные заказа
            
        Returns:
            Обновлённый заказ
        """
        endpoint = f"/api/1/orders/{order_id}"
        data = {**order_data, "organizationId": self.organization_id}
        
        try:
            result = self._make_request("PUT", endpoint, data=data)
            logger.info(f"Заказ {order_id} обновлён")
            return result
        except Exception as e:
            logger.error(f"Ошибка обновления заказа {order_id}: {e}")
            raise
    
    def delete_order(self, order_id: str) -> bool:
        """
        Удаление заказа
        
        Документация: https://api-ru.iiko.services/#operation/DeleteOrder
        
        Args:
            order_id: ID заказа
            
        Returns:
            True если заказ успешно удалён
        """
        endpoint = f"/api/1/orders/{order_id}"
        params = {"organizationId": self.organization_id}
        
        try:
            self._make_request("DELETE", endpoint, params=params)
            logger.info(f"Заказ {order_id} удалён")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления заказа {order_id}: {e}")
            raise
    
    def get_orders(self, date_from: Optional[str] = None, 
                   date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Получение списка заказов
        
        Документация: https://api-ru.iiko.services/#operation/GetOrders
        
        Args:
            date_from: Дата начала периода (формат: YYYY-MM-DD)
            date_to: Дата окончания периода (формат: YYYY-MM-DD)
            
        Returns:
            Список заказов
        """
        endpoint = "/api/1/orders"
        params = {"organizationId": self.organization_id}
        
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result.get("orders", [])
        except Exception as e:
            logger.error(f"Ошибка получения заказов: {e}")
            raise

class IikoCustomersClient(BaseApiClient):
    """Клиент для работы с клиентами"""
    
    def __init__(self, base_url: str, api_key: str, organization_id: str):
        super().__init__(base_url, api_key)
        self.organization_id = organization_id
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создание нового клиента
        
        Документация: https://api-ru.iiko.services/#operation/CreateCustomer
        
        Args:
            customer_data: Данные клиента
            
        Returns:
            Созданный клиент
        """
        endpoint = "/api/1/customers"
        data = {**customer_data, "organizationId": self.organization_id}
        
        try:
            result = self._make_request("POST", endpoint, data=data)
            logger.info(f"Клиент создан: {result.get('id')}")
            return result
        except Exception as e:
            logger.error(f"Ошибка создания клиента: {e}")
            raise
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Получение информации о клиенте
        
        Документация: https://api-ru.iiko.services/#operation/GetCustomer
        
        Args:
            customer_id: ID клиента
            
        Returns:
            Информация о клиенте
        """
        endpoint = f"/api/1/customers/{customer_id}"
        params = {"organizationId": self.organization_id}
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result
        except Exception as e:
            logger.error(f"Ошибка получения клиента {customer_id}: {e}")
            raise
    
    def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обновление клиента
        
        Документация: https://api-ru.iiko.services/#operation/UpdateCustomer
        
        Args:
            customer_id: ID клиента
            customer_data: Новые данные клиента
            
        Returns:
            Обновлённый клиент
        """
        endpoint = f"/api/1/customers/{customer_id}"
        data = {**customer_data, "organizationId": self.organization_id}
        
        try:
            result = self._make_request("PUT", endpoint, data=data)
            logger.info(f"Клиент {customer_id} обновлён")
            return result
        except Exception as e:
            logger.error(f"Ошибка обновления клиента {customer_id}: {e}")
            raise
    
    def get_customers(self) -> List[Dict[str, Any]]:
        """
        Получение списка клиентов
        
        Документация: https://api-ru.iiko.services/#operation/GetCustomers
        
        Returns:
            Список клиентов
        """
        endpoint = "/api/1/customers"
        params = {"organizationId": self.organization_id}
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result.get("customers", [])
        except Exception as e:
            logger.error(f"Ошибка получения клиентов: {e}")
            raise

class IikoDeliveriesClient(BaseApiClient):
    """Клиент для работы с доставками"""
    
    def __init__(self, base_url: str, api_key: str, organization_id: str):
        super().__init__(base_url, api_key)
        self.organization_id = organization_id
    
    def create_delivery(self, delivery_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создание доставки
        
        Документация: https://api-ru.iiko.services/#operation/CreateDelivery
        
        Args:
            delivery_data: Данные доставки
            
        Returns:
            Созданная доставка
        """
        endpoint = "/api/1/deliveries"
        data = {**delivery_data, "organizationId": self.organization_id}
        
        try:
            result = self._make_request("POST", endpoint, data=data)
            logger.info(f"Доставка создана: {result.get('id')}")
            return result
        except Exception as e:
            logger.error(f"Ошибка создания доставки: {e}")
            raise
    
    def get_delivery(self, delivery_id: str) -> Dict[str, Any]:
        """
        Получение информации о доставке
        
        Документация: https://api-ru.iiko.services/#operation/GetDelivery
        
        Args:
            delivery_id: ID доставки
            
        Returns:
            Информация о доставке
        """
        endpoint = f"/api/1/deliveries/{delivery_id}"
        params = {"organizationId": self.organization_id}
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result
        except Exception as e:
            logger.error(f"Ошибка получения доставки {delivery_id}: {e}")
            raise
    
    def update_delivery(self, delivery_id: str, delivery_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обновление доставки
        
        Документация: https://api-ru.iiko.services/#operation/UpdateDelivery
        
        Args:
            delivery_id: ID доставки
            delivery_data: Новые данные доставки
            
        Returns:
            Обновлённая доставка
        """
        endpoint = f"/api/1/deliveries/{delivery_id}"
        data = {**delivery_data, "organizationId": self.organization_id}
        
        try:
            result = self._make_request("PUT", endpoint, data=data)
            logger.info(f"Доставка {delivery_id} обновлена")
            return result
        except Exception as e:
            logger.error(f"Ошибка обновления доставки {delivery_id}: {e}")
            raise
    
    def get_deliveries(self, date_from: Optional[str] = None, 
                       date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Получение списка доставок
        
        Документация: https://api-ru.iiko.services/#operation/GetDeliveries
        
        Args:
            date_from: Дата начала периода (формат: YYYY-MM-DD)
            date_to: Дата окончания периода (формат: YYYY-MM-DD)
            
        Returns:
            Список доставок
        """
        endpoint = "/api/1/deliveries"
        params = {"organizationId": self.organization_id}
        
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result.get("deliveries", [])
        except Exception as e:
            logger.error(f"Ошибка получения доставок: {e}")
            raise

class IikoReservesClient(BaseApiClient):
    """Клиент для работы с резервами"""
    
    def __init__(self, base_url: str, api_key: str, organization_id: str):
        super().__init__(base_url, api_key)
        self.organization_id = organization_id
    
    def create_reserve(self, reserve_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создание резерва стола
        
        Документация: https://api-ru.iiko.services/#operation/CreateReserve
        
        Args:
            reserve_data: Данные резерва
            
        Returns:
            Созданный резерв
        """
        endpoint = "/api/1/reserves"
        data = {**reserve_data, "organizationId": self.organization_id}
        
        try:
            result = self._make_request("POST", endpoint, data=data)
            logger.info(f"Резерв создан: {result.get('id')}")
            return result
        except Exception as e:
            logger.error(f"Ошибка создания резерва: {e}")
            raise
    
    def get_reserve(self, reserve_id: str) -> Dict[str, Any]:
        """
        Получение информации о резерве
        
        Документация: https://api-ru.iiko.services/#operation/GetReserve
        
        Args:
            reserve_id: ID резерва
            
        Returns:
            Информация о резерве
        """
        endpoint = f"/api/1/reserves/{reserve_id}"
        params = {"organizationId": self.organization_id}
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result
        except Exception as e:
            logger.error(f"Ошибка получения резерва {reserve_id}: {e}")
            raise
    
    def update_reserve(self, reserve_id: str, reserve_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обновление резерва
        
        Документация: https://api-ru.iiko.services/#operation/UpdateReserve
        
        Args:
            reserve_id: ID резерва
            reserve_data: Новые данные резерва
            
        Returns:
            Обновлённый резерв
        """
        endpoint = f"/api/1/reserves/{reserve_id}"
        data = {**reserve_data, "organizationId": self.organization_id}
        
        try:
            result = self._make_request("PUT", endpoint, data=data)
            logger.info(f"Резерв {reserve_id} обновлён")
            return result
        except Exception as e:
            logger.error(f"Ошибка обновления резерва {reserve_id}: {e}")
            raise
    
    def cancel_reserve(self, reserve_id: str) -> bool:
        """
        Отмена резерва
        
        Документация: https://api-ru.iiko.services/#operation/CancelReserve
        
        Args:
            reserve_id: ID резерва
            
        Returns:
            True если резерв успешно отменён
        """
        endpoint = f"/api/1/reserves/{reserve_id}/cancel"
        params = {"organizationId": self.organization_id}
        
        try:
            self._make_request("POST", endpoint, params=params)
            logger.info(f"Резерв {reserve_id} отменён")
            return True
        except Exception as e:
            logger.error(f"Ошибка отмены резерва {reserve_id}: {e}")
            raise
    
    def get_reserves(self, date_from: Optional[str] = None, 
                     date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Получение списка резервов
        
        Документация: https://api-ru.iiko.services/#operation/GetReserves
        
        Args:
            date_from: Дата начала периода (формат: YYYY-MM-DD)
            date_to: Дата окончания периода (формат: YYYY-MM-DD)
            
        Returns:
            Список резервов
        """
        endpoint = "/api/1/reserves"
        params = {"organizationId": self.organization_id}
        
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result.get("reserves", [])
        except Exception as e:
            logger.error(f"Ошибка получения резервов: {e}")
            raise

class IikoReportsClient(BaseApiClient):
    """Клиент для работы с отчётами"""
    
    def __init__(self, base_url: str, api_key: str, organization_id: str):
        super().__init__(base_url, api_key)
        self.organization_id = organization_id
    
    def get_sales_report(self, date_from: Optional[str] = None, 
                         date_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Получение отчёта по продажам
        
        Документация: https://api-ru.iiko.services/#operation/GetSalesReport
        
        Args:
            date_from: Дата начала периода (формат: YYYY-MM-DD)
            date_to: Дата окончания периода (формат: YYYY-MM-DD)
            
        Returns:
            Отчёт по продажам
        """
        endpoint = "/api/1/reports/sales"
        params = {"organizationId": self.organization_id}
        
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result
        except Exception as e:
            logger.error(f"Ошибка получения отчёта по продажам: {e}")
            raise
    
    def get_products_report(self, date_from: Optional[str] = None, 
                           date_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Получение отчёта по товарам
        
        Документация: https://api-ru.iiko.services/#operation/GetProductsReport
        
        Args:
            date_from: Дата начала периода (формат: YYYY-MM-DD)
            date_to: Дата окончания периода (формат: YYYY-MM-DD)
            
        Returns:
            Отчёт по товарам
        """
        endpoint = "/api/1/reports/products"
        params = {"organizationId": self.organization_id}
        
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        
        try:
            result = self._make_request("GET", endpoint, params=params)
            return result
        except Exception as e:
            logger.error(f"Ошибка получения отчёта по товарам: {e}")
            raise

class IikoMainClient:
    """Основной клиент для работы с API iiko"""
    
    def __init__(self, api_key: str, organization_id: Optional[str] = None):
        self.base_url = "https://api-ru.iiko.services"
        self.api_key = api_key
        self.organization_id = organization_id
        
        # Инициализация клиентов
        self.auth = IikoAuthClient(self.base_url, self.api_key)
        self.organizations = IikoOrganizationsClient(self.base_url, self.api_key)
        
        if organization_id:
            self._init_organization_clients()
    
    def _init_organization_clients(self):
        """Инициализация клиентов, требующих organization_id"""
        if not self.organization_id:
            raise ValidationError("ID организации не установлен")
        
        self.menu = IikoMenuClient(self.base_url, self.api_key, self.organization_id)
        self.orders = IikoOrdersClient(self.base_url, self.api_key, self.organization_id)
        self.customers = IikoCustomersClient(self.base_url, self.api_key, self.organization_id)
        self.deliveries = IikoDeliveriesClient(self.base_url, self.api_key, self.organization_id)
        self.reserves = IikoReservesClient(self.base_url, self.api_key, self.organization_id)
        self.reports = IikoReportsClient(self.base_url, self.api_key, self.organization_id)
    
    def set_organization(self, organization_id: str):
        """Установка ID организации"""
        self.organization_id = organization_id
        self._init_organization_clients()
        logger.info(f"ID организации установлен: {organization_id}")
    
    def check_connection(self) -> bool:
        """Проверка соединения с API"""
        try:
            self.organizations.get_organizations()
            logger.info("Соединение с API установлено")
            return True
        except Exception as e:
            logger.error(f"Ошибка соединения с API: {e}")
            return False

# ==================== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ООП ВЕРСИИ ====================

def example_oop_usage():
    """Пример использования ООП версии API"""
    print("=== Пример использования ООП версии iiko API ===")
    
    # Создание клиента
    client = IikoMainClient("your_api_key_here")
    
    # Проверка соединения
    if client.check_connection():
        print("✓ Соединение установлено")
        
        # Получение списка организаций
        try:
            orgs = client.organizations.get_organizations()
            print(f"✓ Найдено организаций: {len(orgs)}")
            
            if orgs:
                # Установка первой организации
                first_org = orgs[0]
                client.set_organization(first_org['id'])
                print(f"✓ Установлена организация: {first_org['name']}")
                
                # Получение меню
                menu = client.menu.get_menu()
                print(f"✓ Получено товаров в меню: {len(menu)}")
                
                # Создание заказа
                order_data = ORDER_CREATE_EXAMPLE.copy()
                order_data["organizationId"] = first_org['id']
                
                order = client.orders.create_order(order_data)
                print(f"✓ Заказ создан с ID: {order['id']}")
                
        except Exception as e:
            print(f"✗ Ошибка: {e}")
    else:
        print("✗ Соединение не установлено")

if __name__ == "__main__":
    example_oop_usage()
