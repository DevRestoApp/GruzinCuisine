"""
Примеры данных для API iiko
Документация: https://api-ru.iiko.services
"""

# ==================== АУТЕНТИФИКАЦИЯ ====================

AUTH_RESPONSE_EXAMPLE = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires": "2024-12-31T23:59:59.000Z"
}

# ==================== ОРГАНИЗАЦИИ ====================

ORGANIZATIONS_LIST_EXAMPLE = {
    "organizations": [
        {
            "id": "12345678-1234-1234-1234-123456789012",
            "name": "Ресторан 'Грузинская кухня'",
            "type": "Restaurant",
            "address": "ул. Тверская, 1, Москва",
            "phone": "+7 (495) 123-45-67",
            "email": "info@gruzin-cuisine.ru",
            "timeZone": "Europe/Moscow",
            "currency": "RUB",
            "isActive": True
        },
        {
            "id": "87654321-4321-4321-4321-210987654321",
            "name": "Кафе 'Тбилиси'",
            "type": "Cafe",
            "address": "ул. Арбат, 15, Москва",
            "phone": "+7 (495) 987-65-43",
            "email": "info@tbilisi-cafe.ru",
            "timeZone": "Europe/Moscow",
            "currency": "RUB",
            "isActive": True
        }
    ]
}

ORGANIZATION_BY_ID_EXAMPLE = {
    "id": "12345678-1234-1234-1234-123456789012",
    "name": "Ресторан 'Грузинская кухня'",
    "type": "Restaurant",
    "address": "ул. Тверская, 1, Москва",
    "phone": "+7 (495) 123-45-67",
    "email": "info@gruzin-cuisine.ru",
    "timeZone": "Europe/Moscow",
    "currency": "RUB",
    "isActive": True,
    "settings": {
        "delivery": True,
        "reservation": True,
        "takeaway": True
    }
}

# ==================== МЕНЮ И ТОВАРЫ ====================

MENU_EXAMPLE = {
    "items": [
        {
            "id": "dish-001",
            "name": "Хачапури по-аджарски",
            "description": "Традиционный грузинский пирог с яйцом и сыром",
            "price": 450.0,
            "category": "Основные блюда",
            "imageUrl": "https://example.com/khachapuri.jpg",
            "isAvailable": True,
            "nutritionalInfo": {
                "calories": 320,
                "proteins": 12.5,
                "fats": 18.2,
                "carbohydrates": 28.1
            }
        },
        {
            "id": "dish-002",
            "name": "Хинкали",
            "description": "Грузинские пельмени с мясом и бульоном",
            "price": 380.0,
            "category": "Основные блюда",
            "imageUrl": "https://example.com/khinkali.jpg",
            "isAvailable": True,
            "nutritionalInfo": {
                "calories": 280,
                "proteins": 15.8,
                "fats": 12.4,
                "carbohydrates": 22.6
            }
        }
    ]
}

PRODUCTS_LIST_EXAMPLE = {
    "products": [
        {
            "id": "prod-001",
            "name": "Хачапури по-аджарски",
            "description": "Традиционный грузинский пирог",
            "price": 450.0,
            "costPrice": 180.0,
            "category": "Основные блюда",
            "isActive": True,
            "modifiers": [
                {
                    "id": "mod-001",
                    "name": "Дополнительный сыр",
                    "price": 50.0
                }
            ]
        }
    ]
}

PRODUCT_BY_ID_EXAMPLE = {
    "id": "prod-001",
    "name": "Хачапури по-аджарски",
    "description": "Традиционный грузинский пирог с яйцом и сыром",
    "price": 450.0,
    "costPrice": 180.0,
    "category": "Основные блюда",
    "isActive": True,
    "imageUrl": "https://example.com/khachapuri.jpg",
    "modifiers": [
        {
            "id": "mod-001",
            "name": "Дополнительный сыр",
            "price": 50.0
        }
    ],
    "nutritionalInfo": {
        "calories": 320,
        "proteins": 12.5,
        "fats": 18.2,
        "carbohydrates": 28.1
    }
}

# ==================== ЗАКАЗЫ ====================

ORDER_CREATE_REQUEST_EXAMPLE = {
    "organizationId": "12345678-1234-1234-1234-123456789012",
    "items": [
        {
            "productId": "prod-001",
            "amount": 2,
            "price": 450.0,
            "modifiers": [
                {
                    "id": "mod-001",
                    "amount": 1,
                    "price": 50.0
                }
            ]
        }
    ],
    "customerPhone": "+79001234567",
    "customerName": "Иван Иванов",
    "deliveryPoint": {
        "address": "ул. Тверская, 10, кв. 5",
        "latitude": 55.7558,
        "longitude": 37.6176
    },
    "deliveryType": "Delivery",
    "paymentType": "Card",
    "comment": "Доставить к 19:00"
}

ORDER_RESPONSE_EXAMPLE = {
    "id": "order-12345",
    "number": "0001",
    "status": "New",
    "items": [
        {
            "id": "item-001",
            "productId": "prod-001",
            "productName": "Хачапури по-аджарски",
            "amount": 2,
            "price": 450.0,
            "sum": 900.0,
            "modifiers": [
                {
                    "id": "mod-001",
                    "name": "Дополнительный сыр",
                    "amount": 1,
                    "price": 50.0,
                    "sum": 50.0
                }
            ]
        }
    ],
    "customerPhone": "+79001234567",
    "customerName": "Иван Иванов",
    "deliveryPoint": {
        "address": "ул. Тверская, 10, кв. 5",
        "latitude": 55.7558,
        "longitude": 37.6176
    },
    "deliveryType": "Delivery",
    "paymentType": "Card",
    "sum": 950.0,
    "comment": "Доставить к 19:00",
    "createdDate": "2024-01-15T18:30:00.000Z",
    "estimatedDeliveryTime": "2024-01-15T19:00:00.000Z"
}

ORDERS_LIST_EXAMPLE = {
    "orders": [
        {
            "id": "order-12345",
            "number": "0001",
            "status": "New",
            "sum": 950.0,
            "customerPhone": "+79001234567",
            "deliveryType": "Delivery",
            "createdDate": "2024-01-15T18:30:00.000Z"
        },
        {
            "id": "order-12346",
            "number": "0002",
            "status": "InProgress",
            "sum": 650.0,
            "customerPhone": "+79001234568",
            "deliveryType": "Takeaway",
            "createdDate": "2024-01-15T18:45:00.000Z"
        }
    ]
}

# ==================== КЛИЕНТЫ ====================

CUSTOMER_CREATE_REQUEST_EXAMPLE = {
    "name": "Иван Иванов",
    "phone": "+79001234567",
    "email": "ivan@example.com",
    "birthDate": "1990-05-15",
    "address": "ул. Тверская, 10, кв. 5",
    "comment": "Постоянный клиент"
}

CUSTOMER_RESPONSE_EXAMPLE = {
    "id": "customer-001",
    "name": "Иван Иванов",
    "phone": "+79001234567",
    "email": "ivan@example.com",
    "birthDate": "1990-05-15",
    "address": "ул. Тверская, 10, кв. 5",
    "comment": "Постоянный клиент",
    "createdDate": "2024-01-01T10:00:00.000Z",
    "lastVisitDate": "2024-01-15T18:30:00.000Z",
    "totalOrders": 15,
    "totalSpent": 12500.0
}

CUSTOMERS_LIST_EXAMPLE = {
    "customers": [
        {
            "id": "customer-001",
            "name": "Иван Иванов",
            "phone": "+79001234567",
            "email": "ivan@example.com",
            "totalOrders": 15,
            "totalSpent": 12500.0
        },
        {
            "id": "customer-002",
            "name": "Мария Петрова",
            "phone": "+79001234568",
            "email": "maria@example.com",
            "totalOrders": 8,
            "totalSpent": 6800.0
        }
    ]
}

# ==================== СКЛАДЫ И ОСТАТКИ ====================

WAREHOUSES_LIST_EXAMPLE = {
    "warehouses": [
        {
            "id": "warehouse-001",
            "name": "Основной склад",
            "address": "ул. Складская, 1, Москва",
            "isActive": True,
            "type": "Main"
        },
        {
            "id": "warehouse-002",
            "name": "Склад готовой продукции",
            "address": "ул. Производственная, 5, Москва",
            "isActive": True,
            "type": "Production"
        }
    ]
}

STOCK_EXAMPLE = {
    "stock": [
        {
            "productId": "prod-001",
            "productName": "Хачапури по-аджарски",
            "warehouseId": "warehouse-001",
            "warehouseName": "Основной склад",
            "amount": 25,
            "unit": "шт",
            "minAmount": 5,
            "maxAmount": 100
        },
        {
            "productId": "prod-002",
            "productName": "Хинкали",
            "warehouseId": "warehouse-001",
            "warehouseName": "Основной склад",
            "amount": 40,
            "unit": "шт",
            "minAmount": 10,
            "maxAmount": 150
        }
    ]
}

# ==================== ОТЧЁТЫ ====================

SALES_REPORT_EXAMPLE = {
    "period": {
        "from": "2024-01-01T00:00:00.000Z",
        "to": "2024-01-31T23:59:59.000Z"
    },
    "summary": {
        "totalOrders": 1250,
        "totalRevenue": 187500.0,
        "averageOrderValue": 150.0,
        "totalCustomers": 450
    },
    "byCategory": [
        {
            "category": "Основные блюда",
            "orders": 850,
            "revenue": 127500.0,
            "percentage": 68.0
        },
        {
            "category": "Напитки",
            "orders": 400,
            "revenue": 60000.0,
            "percentage": 32.0
        }
    ]
}

PRODUCTS_REPORT_EXAMPLE = {
    "period": {
        "from": "2024-01-01T00:00:00.000Z",
        "to": "2024-01-31T23:59:59.000Z"
    },
    "topProducts": [
        {
            "productId": "prod-001",
            "productName": "Хачапури по-аджарски",
            "orders": 180,
            "revenue": 81000.0,
            "percentage": 43.2
        },
        {
            "productId": "prod-002",
            "productName": "Хинкали",
            "orders": 150,
            "revenue": 57000.0,
            "percentage": 30.4
        }
    ]
}

# ==================== ДОСТАВКА ====================

DELIVERY_CREATE_REQUEST_EXAMPLE = {
    "organizationId": "12345678-1234-1234-1234-123456789012",
    "orderId": "order-12345",
    "deliveryPoint": {
        "address": "ул. Тверская, 10, кв. 5",
        "latitude": 55.7558,
        "longitude": 37.6176
    },
    "estimatedDeliveryTime": "2024-01-15T19:00:00.000Z",
    "comment": "Доставить к 19:00"
}

DELIVERY_RESPONSE_EXAMPLE = {
    "id": "delivery-001",
    "orderId": "order-12345",
    "status": "New",
    "deliveryPoint": {
        "address": "ул. Тверская, 10, кв. 5",
        "latitude": 55.7558,
        "longitude": 37.6176
    },
    "estimatedDeliveryTime": "2024-01-15T19:00:00.000Z",
    "actualDeliveryTime": None,
    "comment": "Доставить к 19:00",
    "createdDate": "2024-01-15T18:30:00.000Z"
}

DELIVERIES_LIST_EXAMPLE = {
    "deliveries": [
        {
            "id": "delivery-001",
            "orderId": "order-12345",
            "status": "New",
            "estimatedDeliveryTime": "2024-01-15T19:00:00.000Z",
            "createdDate": "2024-01-15T18:30:00.000Z"
        },
        {
            "id": "delivery-002",
            "orderId": "order-12346",
            "status": "InProgress",
            "estimatedDeliveryTime": "2024-01-15T19:30:00.000Z",
            "createdDate": "2024-01-15T18:45:00.000Z"
        }
    ]
}

# ==================== РЕЗЕРВЫ ====================

RESERVE_CREATE_REQUEST_EXAMPLE = {
    "organizationId": "12345678-1234-1234-1234-123456789012",
    "tableId": "table-001",
    "customerName": "Иван Иванов",
    "customerPhone": "+79001234567",
    "guestsCount": 4,
    "reservationDate": "2024-01-20T19:00:00.000Z",
    "comment": "Столик у окна"
}

RESERVE_RESPONSE_EXAMPLE = {
    "id": "reserve-001",
    "tableId": "table-001",
    "tableName": "Стол №1",
    "customerName": "Иван Иванов",
    "customerPhone": "+79001234567",
    "guestsCount": 4,
    "reservationDate": "2024-01-20T19:00:00.000Z",
    "status": "Confirmed",
    "comment": "Столик у окна",
    "createdDate": "2024-01-15T18:30:00.000Z"
}

RESERVES_LIST_EXAMPLE = {
    "reserves": [
        {
            "id": "reserve-001",
            "tableName": "Стол №1",
            "customerName": "Иван Иванов",
            "guestsCount": 4,
            "reservationDate": "2024-01-20T19:00:00.000Z",
            "status": "Confirmed"
        },
        {
            "id": "reserve-002",
            "tableName": "Стол №3",
            "customerName": "Мария Петрова",
            "guestsCount": 2,
            "reservationDate": "2024-01-20T20:00:00.000Z",
            "status": "Confirmed"
        }
    ]
}

# ==================== СТОЛЫ И ЗОНЫ ====================

TABLES_LIST_EXAMPLE = {
    "tables": [
        {
            "id": "table-001",
            "name": "Стол №1",
            "zoneId": "zone-001",
            "zoneName": "Основной зал",
            "seatsCount": 4,
            "isActive": True,
            "status": "Available"
        },
        {
            "id": "table-002",
            "name": "Стол №2",
            "zoneId": "zone-001",
            "zoneName": "Основной зал",
            "seatsCount": 6,
            "isActive": True,
            "status": "Reserved"
        }
    ]
}

ZONES_LIST_EXAMPLE = {
    "zones": [
        {
            "id": "zone-001",
            "name": "Основной зал",
            "description": "Основная обеденная зона",
            "isActive": True,
            "tablesCount": 12
        },
        {
            "id": "zone-002",
            "name": "Летняя веранда",
            "description": "Открытая веранда",
            "isActive": True,
            "tablesCount": 8
        }
    ]
}

# ==================== ПЛАТЕЖИ ====================

PAYMENT_CREATE_REQUEST_EXAMPLE = {
    "organizationId": "12345678-1234-1234-1234-123456789012",
    "orderId": "order-12345",
    "amount": 950.0,
    "paymentType": "Card",
    "paymentMethod": "Visa",
    "comment": "Оплата картой"
}

PAYMENT_RESPONSE_EXAMPLE = {
    "id": "payment-001",
    "orderId": "order-12345",
    "amount": 950.0,
    "paymentType": "Card",
    "paymentMethod": "Visa",
    "status": "Completed",
    "comment": "Оплата картой",
    "createdDate": "2024-01-15T18:30:00.000Z",
    "completedDate": "2024-01-15T18:31:00.000Z"
}

PAYMENTS_LIST_EXAMPLE = {
    "payments": [
        {
            "id": "payment-001",
            "orderId": "order-12345",
            "amount": 950.0,
            "paymentType": "Card",
            "status": "Completed",
            "createdDate": "2024-01-15T18:30:00.000Z"
        },
        {
            "id": "payment-002",
            "orderId": "order-12346",
            "amount": 650.0,
            "paymentType": "Cash",
            "status": "Completed",
            "createdDate": "2024-01-15T18:45:00.000Z"
        }
    ]
}

# ==================== СКИДКИ И АКЦИИ ====================

DISCOUNTS_LIST_EXAMPLE = {
    "discounts": [
        {
            "id": "discount-001",
            "name": "Скидка 10% на первый заказ",
            "description": "Скидка 10% для новых клиентов",
            "percentage": 10.0,
            "isActive": True,
            "validFrom": "2024-01-01T00:00:00.000Z",
            "validTo": "2024-12-31T23:59:59.000Z"
        },
        {
            "id": "discount-002",
            "name": "Скидка 15% на доставку",
            "description": "Скидка на доставку при заказе от 1000 руб.",
            "percentage": 15.0,
            "isActive": True,
            "minOrderAmount": 1000.0
        }
    ]
}

PROMOTIONS_LIST_EXAMPLE = {
    "promotions": [
        {
            "id": "promo-001",
            "name": "2 по цене 1 на хинкали",
            "description": "При заказе 2 порций хинкали вторая бесплатно",
            "type": "BuyOneGetOne",
            "isActive": True,
            "validFrom": "2024-01-01T00:00:00.000Z",
            "validTo": "2024-01-31T23:59:59.000Z"
        },
        {
            "id": "promo-002",
            "name": "Бесплатная доставка",
            "description": "Бесплатная доставка при заказе от 1500 руб.",
            "type": "FreeDelivery",
            "isActive": True,
            "minOrderAmount": 1500.0
        }
    ]
}

# ==================== API ИНФОРМАЦИЯ ====================

API_INFO_EXAMPLE = {
    "version": "1.0.0",
    "name": "iiko API",
    "description": "API для интеграции с системой iiko",
    "documentation": "https://api-ru.iiko.services",
    "endpoints": [
        "/api/1/auth/access_token",
        "/api/1/organizations",
        "/api/1/menu",
        "/api/1/orders",
        "/api/1/customers"
    ],
    "rateLimit": {
        "requestsPerMinute": 1000,
        "requestsPerHour": 50000
    }
}
