import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_get_menu(client):
    response = client.get("/menu")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(item["name"] == "Margherita" for item in data)


def test_create_order(client):
    new_order = {
        "customer": "Flask User",
        "address": "123 Flask St",
        "items": [
            {"pizza": "Margherita", "size": "Medium", "quantity": 1, "extraToppings": ["Cheese"]}
        ],
        "total": 9.50,
        "status": "Preparing",
    }
    response = client.post("/orders", json=new_order)
    assert response.status_code == 200
    data = response.get_json()
    assert data["customer"] == "Flask User"
    assert "orderId" in data
