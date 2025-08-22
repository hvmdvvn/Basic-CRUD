# Pizza Ordering API with Flask

## Overview

This project is a **Pizza Ordering API** built with **Flask**, a lightweight and flexible Python web framework.
The application demonstrates how to build **REST APIs** with CRUD operations, request validation, and API documentation using **Flasgger** (Swagger UI for Flask).

The API provides the following core features:

* Manage pizza orders (Create, Read, Update, Delete).
* View a menu of available pizzas.
* API documentation via Swagger UI (`/apidocs`).

---

## Why Flask?

Flask is often called a **"micro-framework"**, but that does not mean it is less powerful. Instead, Flask provides a minimal core and leaves you free to pick additional libraries as needed. This makes Flask an excellent choice when building APIs like this project.

### Key Features of Flask:

1. **Simplicity & Flexibility**

   * Unlike Django (which enforces a lot of structure), Flask allows you to design the project layout as you see fit.
   * Perfect for projects where you need control and don’t want heavy abstractions.

2. **Lightweight & Fast**

   * Only provides the essentials: routing, request/response handling, and minimal setup.
   * Everything else (ORM, validation, authentication, etc.) can be added as needed.

3. **Integration with Tools**

   * Works well with libraries like **SQLAlchemy**, **Marshmallow**, **Pydantic**, or **Flasgger**.
   * This project uses **Marshmallow (schemas.py)** for validation and **Flasgger** for auto-generated Swagger documentation.

4. **Better for Small to Medium APIs**

   * If you’re building microservices or lightweight APIs, Flask is often a better choice than Django.
   * Django is excellent for large-scale applications with many built-in features (ORM, admin panel, auth system).
   * Flask is better when you want only what you need, without overhead.

---

## Project Structure

```
Basic-CRUD/
│── app.py              # Main Flask app with routes
│── mylib/              # Business logic (CRUD functions, menu, etc.)
│── schemas.py          # Marshmallow schemas for validation
│── requirements.txt    # Python dependencies
│── Makefile            # Commands for running, testing, linting
│── tests/              # Unit tests
│── README.md           # Project documentation
```

---

## Functionalities in This Project

### Endpoints

| Method | Endpoint       | Description                   |
| ------ | -------------- | ----------------------------- |
| GET    | `/orders`      | List all orders               |
| GET    | `/orders/<id>` | Get details of a single order |
| POST   | `/orders`      | Create a new order            |
| PUT    | `/orders/<id>` | Update an existing order      |
| DELETE | `/orders/<id>` | Delete an order               |
| GET    | `/menu`        | Get available pizza menu      |
| GET    | `/apidocs`     | Swagger documentation         |

---

### Libraries Used

1. **Flask** → Core framework for building the API.
2. **Flasgger** → Provides Swagger UI documentation for endpoints.
3. **Marshmallow** → Used in `schemas.py` for validating and serializing order data.
4. **pytest** → For writing and running tests.
5. **flake8 & black** → For linting and formatting code.

---

## Running the Project

### Prerequisites

* Python 3.9+
* Virtual environment (`venv`) recommended

### Installation

```bash
# Clone repo
git clone https://github.com/hvmdvvn/Basic-CRUD.git
cd Basic-CRUD

# Create venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
make install
```

### Run the App

```bash
make run
```

The app will be available at:

* **API:** `http://127.0.0.1:8000`
* **Swagger Docs:** `http://127.0.0.1:8000/apidocs`

---

## Why This Flask App is a Good Example

* Shows how to build **CRUD APIs** using Flask routes.
* Demonstrates **schema validation** with Marshmallow (Flask doesn’t enforce schemas like FastAPI).
* Uses **Flasgger** to auto-generate Swagger documentation.
* Includes a **Makefile** for automation (run, test, lint, clean).
* Lightweight and extensible — you can easily add a database (SQLAlchemy), authentication, or deployment (Docker).

---

## Future Improvements

* Add **database support** with SQLAlchemy.
* Implement **authentication & authorization** (JWT).
* Add **Dockerfile** and CI/CD pipeline.
* Enhance validation with **Flask-Pydantic**.

---

## Conclusion

Flask is an excellent choice for building REST APIs when you want:

* Full control over the architecture.
* Lightweight, fast applications.
* Easy integration with external libraries.

This project showcases a practical implementation of a **Flask REST API with CRUD operations**, request validation, and Swagger documentation.

