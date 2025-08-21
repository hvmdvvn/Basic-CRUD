import uvicorn
from fastapi import FastAPI
from typing import List
from mylib import (
    create_order,
    update_order,
    delete_order,
    get_order,
    list_orders,
    get_menu,
)
from schemas import Order, OrderCreate, OrderUpdate

app = FastAPI(title="Pizza Ordering API", version="1.0")

# ---------- Orders Endpoints ----------


@app.get("/orders", response_model=List[Order])
def read_orders():
    return list_orders()


@app.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int):
    order = get_order(order_id)
    if order:
        return order
    return {"error": "Order not found"}


@app.post("/orders", response_model=Order)
def add_order(order: OrderCreate):
    return create_order(order.dict())


@app.put("/orders/{order_id}", response_model=Order)
def modify_order(order_id: int, order: OrderUpdate):
    updated = update_order(order_id, order.dict())
    if updated:
        return updated
    return {"error": "Order not found"}


@app.delete("/orders/{order_id}")
def remove_order(order_id: int):
    return delete_order(order_id)


# ---------- Menu Endpoint ----------


@app.get("/menu")
def menu():
    return get_menu()


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
