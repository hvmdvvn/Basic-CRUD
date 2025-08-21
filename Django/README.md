# Pizza Ordering API (Django + DRF)

This project is a basic CRUD API for managing pizza orders and viewing the menu, built using **Django** and **Django REST Framework (DRF)**.  
It also includes API documentation with Swagger and ReDoc using `drf-yasg`.

---

## About Django

[Django](https://www.djangoproject.com/) is a **high-level Python web framework** that encourages rapid development and clean, pragmatic design.  
It handles many common web development tasks, such as authentication, database management, and routing, so developers can focus on building features instead of reinventing the wheel.

In this project:

- **Django** provides the core backend framework, ORM, and admin interface.
- **Django REST Framework (DRF)** makes it easy to build RESTful APIs for handling requests and responses in JSON.
- **drf-yasg** is used to generate interactive API documentation (Swagger UI and ReDoc).

---

## Project Structure

```

Django/
├── pizza\_project/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── orders/                # Orders app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── crud.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   └── pizza\_project/         # Main project settings
│       ├── settings.py
│       ├── urls.py
├── requirements.txt
├── Makefile
└── README.md

````

---

## Installation

1. Clone the repository and navigate to the Django folder:

```bash
git clone <repo-url>
cd Basic-CRUD/Django
````

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Using the provided Makefile:

```bash
make run
```

The server will start at:
`http://localhost:8000/`

---

## API Documentation

Swagger and ReDoc are available at:

* Swagger UI: `http://localhost:8000/docs/`
* ReDoc: `http://localhost:8000/redoc/`

---

## Makefile Commands

* `make run` – Run the development server
* `make migrate` – Apply database migrations
* `make makemigrations` – Create new migrations
* `make superuser` – Create an admin superuser
* `make test` – Run tests with pytest
* `make lint` – Run flake8 linter

---

## Running Tests

You can run tests either via Django or pytest:

```bash
make test
```

or

```bash
cd pizza_project
python manage.py test
```

---

## Endpoints

* `GET /orders/` – List all orders
* `GET /orders/<id>/` – Retrieve a specific order
* `POST /orders/` – Create a new order
* `PUT /orders/<id>/` – Update an existing order
* `DELETE /orders/<id>/` – Delete an order
* `GET /orders/menu/` – Get menu items
