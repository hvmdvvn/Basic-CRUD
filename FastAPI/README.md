# FastAPI Pizza Ordering CRUD App

## About the Project
This project is a Pizza Ordering System built with [FastAPI](https://fastapi.tiangolo.com/).  
It demonstrates how to create a simple CRUD (Create, Read, Update, Delete) API using FastAPI and Pydantic models.

The API allows:
- Viewing the menu of pizzas
- Creating new orders
- Viewing all orders
- Updating an order (e.g., change address, items, or status)
- Deleting an order

It is a lightweight project that shows how FastAPI can be used to quickly build and test RESTful APIs.

---

## Why FastAPI?
FastAPI is a modern Python framework for building APIs, designed with speed and developer experience in mind.

- High performance (built on Starlette and Pydantic)  
- Automatic interactive API documentation (Swagger UI and ReDoc)  
- Data validation and type checking built-in  
- Easy to use and beginner-friendly  
- Widely used in production systems  

---

## Project Structure
```

FastAPI/
│── app.py            # Main FastAPI application
│── mylib.py          # Helper library with logic
│── tests.py          # Test cases for API endpoints
│── Makefile          # Automation commands (run, test)
│── requirements.txt  # Python dependencies
│── .github/workflows/fastapi.yml  # CI pipeline

````

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Basic-CRUD.git
cd Basic-CRUD/FastAPI
````

### 2. Create Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```

### 3. Run the Application

```bash
make run
```

The server will start at:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

Interactive API documentation:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Running Tests

This project uses **pytest** with FastAPI's `TestClient`.

```bash
make test
```

---

## Continuous Integration (CI)

GitHub Actions workflow (`fastapi.yml`) is included.
It runs the test suite automatically every time code is pushed or a pull request is made.

---

## Future Improvements

* Connect with a real database (e.g., PostgreSQL, SQLite)
* Add authentication and user accounts
* Extend menu and order management features
* Deploy on cloud platforms (Heroku, AWS, etc.)


