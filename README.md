# RESTful Pizza API — Concepts and Frameworks (FastAPI vs Django REST Framework vs Flask)

This repository contains a simple Pizza Ordering API and serves as a reference for building RESTful backends in Python. This document explains:

* What REST APIs are and how CRUD maps to HTTP
* How HTTPS works and why it matters
* A practical, detailed comparison of **FastAPI**, **Django + Django REST Framework (DRF)**, and **Flask**
* Example snippets, testing, security, and deployment notes

---

## 1) REST API Fundamentals

A **REST API** (Representational State Transfer) exposes **resources** (e.g., `/orders`, `/menu`) over **HTTP** using uniform interfaces. Clients manipulate resources via standard HTTP methods and receive representations (usually JSON).

### Core principles

* **Resources & URIs**: Each resource has a stable URL (`/orders/123`).
* **Statelessness**: Requests carry all needed context (tokens, parameters). Server does not persist client session state between requests.
* **Uniform interface**: Standard HTTP verbs and status codes.
* **Cacheable**: Responses can declare caching headers (e.g., `Cache-Control`, `ETag`).
* **Layered system**: Proxies, gateways, and load balancers may sit between clients and servers.

### HTTP verbs, safety, and idempotency

| Operation      | HTTP Method           | Safe? | Idempotent?    | Typical Status Codes |
| -------------- | --------------------- | ----- | -------------- | -------------------- |
| Read list      | GET `/orders`         | Yes   | Yes            | 200                  |
| Read one       | GET `/orders/{id}`    | Yes   | Yes            | 200, 404             |
| Create         | POST `/orders`        | No    | No             | 201, 400             |
| Replace        | PUT `/orders/{id}`    | No    | Yes            | 200/204, 400, 404    |
| Partial update | PATCH `/orders/{id}`  | No    | Not guaranteed | 200/204, 400, 404    |
| Delete         | DELETE `/orders/{id}` | No    | Yes            | 200/204, 404         |

**Safe** means it does not change server state. **Idempotent** means repeated identical requests yield the same result.

### Common patterns

* **Filtering/Sorting/Pagination**: `/orders?status=delivered&sort=-created_at&page=2&page_size=20`
* **Errors**: Use consistent JSON errors, e.g. `{ "detail": "Not found" }`.
* **Versioning**: Path (`/v1/orders`), header (`Accept: application/vnd.myapi.v1+json`), or subdomain.
* **OpenAPI**: Machine-readable API schema for codegen and docs (Swagger UI/ReDoc).

---

## 2) HTTPS in Practice

**HTTPS** is HTTP over TLS. It ensures:

* **Confidentiality**: Traffic is encrypted.
* **Integrity**: Prevents tampering in transit.
* **Authentication**: Certificates assert server identity.

### Key elements

* **TLS handshake**: Negotiates ciphers, exchanges keys.
* **Certificates**: Issued by a CA (e.g., via Let’s Encrypt with ACME).
* **HSTS**: Enforce HTTPS with the `Strict-Transport-Security` header.
* **HTTP/2 and HTTP/3**: Multiplexing, lower latency.
* **Mutual TLS (mTLS)**: Optional client certificates for service-to-service auth.

### Deployment patterns

* Terminate TLS at a **reverse proxy** (e.g., Nginx, Traefik, Cloud Load Balancer).
* Run your Python app behind the proxy (Gunicorn/Uvicorn/Daphne).

---

## 3) CRUD Operations and Data Modeling

**CRUD** maps to REST endpoints as shown above. Keep payloads predictable with a schema:

```json
{
  "customer": "Alice Smith",
  "address": "123 Main St",
  "items": [
    {"pizza": "Margherita", "size": "Large", "quantity": 1, "extraToppings": ["Olives", "Mushrooms"]},
    {"pizza": "Pepperoni", "size": "Medium", "quantity": 2, "extraToppings": []}
  ],
  "total": 32.50,
  "status": "Preparing"
}
```

Validation and serialization help enforce types, ranges (e.g., `quantity >= 1`), and business rules.

---

## 4) Frameworks Overview

### FastAPI

**Model**: ASGI-first, async-native, built on Starlette.
**Validation**: Pydantic models (v2 in modern versions) for request/response schemas and type hints.
**Docs**: Automatic OpenAPI with Swagger UI and ReDoc out of the box.
**Performance**: Excellent for I/O-bound workloads due to async.
**Learning curve**: Very friendly for typed Python.
**Ecosystem**: Great for microservices and modern APIs.
**Server**: Uvicorn/Hypercorn.

**Minimal example:**

```python
# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    pizza: str
    size: str
    quantity: int
    extraToppings: Optional[List[str]] = []

class Order(BaseModel):
    customer: str
    address: str
    items: List[Item]
    total: float
    status: str

app = FastAPI()

DB = {}
NEXT_ID = 1001

@app.get("/orders")
def list_orders():
    return list(DB.values())

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return DB.get(order_id) or {"detail": "Not found"}

@app.post("/orders", status_code=201)
def create_order(order: Order):
    global NEXT_ID
    DB[NEXT_ID] = {"orderId": NEXT_ID, **order.dict()}
    NEXT_ID += 1
    return DB[NEXT_ID - 1]
```

Run: `uvicorn app:app --reload`

**Strengths**

* Async-first, very fast development and runtime for APIs
* Strong typing and validation with clean function signatures
* Auto docs require no extra setup

**Trade-offs**

* Less batteries-included for monolith features (admin, ORM, templating). You will pick your own stack (SQLModel/SQLAlchemy, auth libs, etc.).

---

### Django + Django REST Framework (DRF)

**Model**: Full-featured web framework; DRF adds REST abstractions.
**Validation/Serialization**: DRF serializers; rich viewsets/routers.
**Docs**: Browsable API included; schema with `drf-spectacular` or `drf-yasg`.
**Batteries included**: ORM, migrations, admin, auth, sessions, templating.
**Async**: Django supports async views; DRF is progressively adopting async patterns, but many stacks remain sync-first.
**Best for**: Larger applications/monoliths, complex relational models, admin-heavy needs.

**Minimal example with DRF:**

```python
# orders/serializers.py
from rest_framework import serializers

class ItemSerializer(serializers.Serializer):
    pizza = serializers.CharField()
    size = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)
    extraToppings = serializers.ListField(child=serializers.CharField(), required=False)

class OrderSerializer(serializers.Serializer):
    customer = serializers.CharField()
    address = serializers.CharField()
    items = ItemSerializer(many=True)
    total = serializers.FloatField()
    status = serializers.CharField()
```

```python
# orders/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer

DB = {}
NEXT_ID = 1001

@api_view(["GET"])
def list_orders(request):
    return Response(list(DB.values()))

@api_view(["GET"])
def get_order(request, order_id: int):
    return Response(DB.get(order_id) or {"detail": "Not found"}, status=200 if order_id in DB else 404)

@api_view(["POST"])
def create_order(request):
    global NEXT_ID
    s = OrderSerializer(data=request.data)
    if s.is_valid():
        DB[NEXT_ID] = {"orderId": NEXT_ID, **s.validated_data}
        NEXT_ID += 1
        return Response(DB[NEXT_ID - 1], status=status.HTTP_201_CREATED)
    return Response(s.errors, status=400)
```

Wire with `urls.py`, install `djangorestframework`, run `python manage.py runserver`.

**Strengths**

* End-to-end stack (ORM, admin, auth) and mature ecosystem
* DRF brings powerful abstraction for complex APIs
* Browsable API speeds up development and QA
* Strong security defaults (CSRF, sessions, permissions)

**Trade-offs**

* Heavier than microframeworks for small services
* Async story is improving but historically sync-first; mixing async and sync requires care

---

### Flask

**Model**: Minimal WSGI microframework; you assemble the pieces.
**Validation**: Use libraries such as Marshmallow (`marshmallow`), Pydantic, or WTForms.
**Docs**: Add-ons like `flask-smorest` can generate OpenAPI.
**Async**: Flask 2+ allows `async def` handlers, but it is still WSGI-first; for native ASGI consider **Quart**.
**Best for**: Small-to-medium services where you prefer minimalism and explicit composition.

**Minimal example:**

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

DB = {}
NEXT_ID = 1001

@app.get("/orders")
def list_orders():
    return jsonify(list(DB.values()))

@app.get("/orders/<int:order_id>")
def get_order(order_id):
    return (jsonify(DB[order_id]), 200) if order_id in DB else (jsonify({"detail": "Not found"}), 404)

@app.post("/orders")
def create_order():
    global NEXT_ID
    data = request.get_json()
    DB[NEXT_ID] = {"orderId": NEXT_ID, **data}
    NEXT_ID += 1
    return jsonify(DB[NEXT_ID - 1]), 201

if __name__ == "__main__":
    app.run(debug=True)
```

**Strengths**

* Extremely simple to start
* Large ecosystem of extensions (Flask-Login, Flask-Admin, Flask-Migrate, SQLAlchemy)
* Fine-grained control over structure

**Trade-offs**

* You assemble and maintain many choices (auth, validation, docs) yourself
* Not async-native; for high-concurrency consider ASGI options or Quart

---

## 5) Feature Comparison

| Feature      | FastAPI                          | Django + DRF                                                             | Flask                                                          |
| ------------ | -------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------- |
| Architecture | ASGI, async-first                | Django framework; DRF for API (sync-first with increasing async support) | WSGI microframework (async-capable routes but not native ASGI) |
| Validation   | Pydantic models                  | DRF serializers                                                          | Marshmallow/Pydantic/hand-rolled                               |
| Auto Docs    | Built-in OpenAPI (Swagger/ReDoc) | Via DRF + `drf-spectacular` or `drf-yasg`                                | Via extensions (e.g., `flask-smorest`)                         |
| ORM          | Choose (SQLAlchemy/SQLModel)     | Built-in Django ORM                                                      | Typically SQLAlchemy                                           |
| Admin        | Not built-in                     | Excellent built-in admin                                                 | Flask-Admin extension                                          |
| Auth         | Extensions (JWT/OAuth)           | Rich auth ecosystem (sessions, tokens, permissions)                      | Extensions (Flask-Login, JWT)                                  |
| Best for     | Microservices, modern APIs       | Full-featured apps/monoliths                                             | Lightweight services and prototypes                            |

---

## 6) Choosing the Right Tool

* **FastAPI**: You want async performance, typed validation, and instant docs for a modern API or microservice. You are comfortable assembling your own ORM/auth.
* **Django + DRF**: You want a full-featured platform with ORM, admin, authentication, and a rich permissions model. Great for complex data models or teams preferring conventions.
* **Flask**: You value minimalism and explicit choices, or need a small service with a simple stack that you compose from extensions.

---

## 7) Testing

* **FastAPI**: `pytest` + `httpx` or FastAPI’s `TestClient` (requests-compatible).
* **Django/DRF**: `pytest-django` or Django’s test runner; DRF’s `APIClient` and `APITestCase`.
* **Flask**: Built-in test client (`app.test_client()`), plus `pytest`.

Example (DRF + pytest):

```python
# tests/test_orders.py
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_create_order():
    client = APIClient()
    payload = {
        "customer": "Test User",
        "address": "123 Test St",
        "items": [{"pizza": "Margherita", "size": "Medium", "quantity": 1, "extraToppings": ["Olives"]}],
        "total": 9.50,
        "status": "Preparing"
    }
    res = client.post("/orders/", payload, format="json")
    assert res.status_code == 201
    assert res.json()["customer"] == "Test User"
```

---

## 8) Security Checklist

* **HTTPS everywhere**; enable HSTS in production.
* **Authentication/Authorization**:

  * JWT or OAuth2 for stateless APIs.
  * Django sessions/permissions for server-rendered or admin use.
* **CORS**: Configure `django-cors-headers` or equivalent if calling from browsers on different origins.
* **CSRF**:

  * Needed for cookie-authenticated browser requests (Django enables by default).
  * Not needed for pure token-auth APIs with `Authorization: Bearer ...`.
* **Input Validation**: Use serializers/models (DRF) or Pydantic (FastAPI).
* **Headers**: Set `Content-Security-Policy` (if serving HTML), `X-Content-Type-Options`, `X-Frame-Options`.
* **Rate limiting**: DRF throttling, reverse proxy rate limit, or libraries (Flask-Limiter).
* **Secrets management**: Environment variables or secret stores; never commit secrets.

---

## 9) Deployment Notes

* **FastAPI (ASGI)**: `gunicorn -k uvicorn.workers.UvicornWorker -w 2 app:app`
* **Django (WSGI/ASGI)**:

  * WSGI: `gunicorn myproj.wsgi:application`
  * ASGI: `daphne myproj.asgi:application` or `uvicorn myproj.asgi:application`
* **Flask (WSGI)**: `gunicorn -w 2 app:app`
* Front with **Nginx/Traefik** for TLS termination, static files, and buffering.
* Containerize with Docker; follow 12-factor principles.
* Health checks: simple `/healthz` endpoint; add readiness/liveness probes in orchestrators.

---

## 10) Local Quickstarts

### FastAPI

```bash
pip install fastapi uvicorn pydantic
uvicorn app:app --reload
# Open http://127.0.0.1:8000/docs
```

### Django + DRF

```bash
pip install django djangorestframework
django-admin startproject pizza_project
cd pizza_project
python manage.py startapp orders
# add 'rest_framework' and 'orders' to INSTALLED_APPS
python manage.py migrate
python manage.py runserver
# Browsable API at your endpoints; add drf-spectacular or drf-yasg for Swagger
```

### Flask

```bash
pip install flask
python app.py
# Open http://127.0.0.1:5000
```

---

## 11) Example API Endpoints (Pizza)

* `GET /orders/` — list orders
* `GET /orders/{id}/` — retrieve an order
* `POST /orders/` — create order
* `PUT /orders/{id}/` — replace order
* `PATCH /orders/{id}/` — partial update
* `DELETE /orders/{id}/` — delete order
* `GET /orders/menu/` — list menu items

Use consistent JSON schemas and validate with serializers/models.

---

## 12) Observability

* **Logging**: Structured logs (JSON) with request IDs.
* **Metrics**: Expose Prometheus metrics or integrate with application performance monitoring tools.
* **Tracing**: OpenTelemetry instrumentation for end-to-end request traces.
* **Error tracking**: Sentry or similar.

---

### Final Notes

* Pick **FastAPI** for modern, typed, async-first APIs with minimal boilerplate and automatic docs.
* Pick **Django + DRF** for full-featured applications with ORM, admin, and robust permissions.
* Pick **Flask** for maximum flexibility with a minimal core and curated extensions.

