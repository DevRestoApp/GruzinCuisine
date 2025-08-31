import requests
import json


def make_request(url, headers, data):
    
    try:
        # Выполняем POST запрос
        response = requests.post(url, headers=headers, json=data)
        
        # Проверяем статус ответа
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            print("Запрос выполнен успешно!")
            print("Ответ API:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка! Статус: {response.status_code}")
            print("Ответ сервера:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON ответа: {e}")
        print("Текстовый ответ:", response.text)

def make_request_get(url, headers):
    
    try:
        # Выполняем POST запрос
        response = requests.get(url, headers=headers)
        
        # Проверяем статус ответа
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            print("Запрос выполнен успешно!")
            print("Ответ API:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка! Статус: {response.status_code}")
            print("Ответ сервера:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON ответа: {e}")
        print("Текстовый ответ:", response.text)

def create_iiko_delivery():
    # URL API
    url = 'https://api-ru.iiko.services/api/1/deliveries/create'
    
    # Заголовки запроса
    headers = {
        'Authorization': 'Bearer ...',
        'Content-Type': 'application/json'
    }
    
    # Данные для отправки
    data = {
        "organizationId": "...",
        "terminalGroupId": "...",
        "order": {
            "externalNumber": 102,
            "orderServiceType": "DeliveryByCourier",
            "customer": {
                "name": "imya",
                "surname": "fam",
                "comment": "komment",
                "email": "test@test.ru"
            },
            "phone": "+79787777777",
            "items": [
                {
                    "productId": "...",
                    "amount": "1",
                    "type": "Product"
                }
            ],
            "payments": [
                {
                    "paymentTypeKind": "Cash",
                    "sum": "349",
                    "paymentTypeId": "..."
                }
            ]
        }
    }

    make_request(url, headers, data)


def get_token(apiLogin: str):
    url = "https://api-ru.iiko.services/api/1/access_token"
    
    headers = {
        # 'Authorization': 'Bearer ...',
        'Content-Type': 'application/json'
    }

    data = {
        "apiLogin": apiLogin
    }

    make_request_get(url, headers, data)


if __name__ == "__main__":
    print("Отправляем запрос к API iiko для создания доставки...")
    get_token()
    # create_iiko_delivery()

