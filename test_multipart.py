import uuid

import requests

BASE_URL = "http://localhost:8000"
test_prod_name = f"Test Product {uuid.uuid4().hex[:6]}"

try:
    res = requests.post(
        f"{BASE_URL}/api/products/",
        data={
            "name": test_prod_name,
            "description": "",
            "price": "25.50",
            "stock": "100",
            "category": "",
        },
    )
    print(res.status_code)
    print(res.json())
except Exception as e:
    print(f"Error: {e}")
