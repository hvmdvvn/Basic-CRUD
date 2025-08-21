import pytest
from fastapi.testclient import TestClient
from app import app 

client = TestClient(app)


def test_get_menu():
    response = client.get("/menu")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["name"] == "Margherita" for item in data)


def test_create_order():
    new_order = {
        "customer": "Test User",
        "address": "123 Test St",
        "items": [
            {
                "pizza": "Margherita",
                "size": "Medium",
                "quantity": 1,
                "extraToppings": ["Olives"],
            }
        ],
        "total": 9.50,
        "status": "Preparing",
    }
    response = client.post("/orders", json=new_order)
    assert response.status_code == 200
    data = response.json()
    assert data["customer"] == "Test User"
    assert "orderId" in data


def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_update_order():
    # Get first order
    orders = client.get("/orders").json()
    order_id = orders[0]["orderId"]

    updated_order = {
        "customer": "Updated User",
        "address": "456 Updated St",
        "items": [
            {"pizza": "Pepperoni", "size": "Large", "quantity": 2, "extraToppings": []}
        ],
        "total": 24.00,
        "status": "Delivered",
    }

    response = client.put(f"/orders/{order_id}", json=updated_order)
    assert response.status_code == 200
    data = response.json()
    assert data["customer"] == "Updated User"


def test_delete_order():
    # Create an order first
    new_order = {
        "customer": "Delete Me",
        "address": "Nowhere",
        "items": [
            {"pizza": "Veggie", "size": "Small", "quantity": 1, "extraToppings": []}
        ],
        "total": 7.75,
        "status": "Preparing",
    }
    order = client.post("/orders", json=new_order).json()
    order_id = order["orderId"]

    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "deleted"
