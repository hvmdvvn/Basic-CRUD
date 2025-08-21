import json
import os

DATA_FILE = "../pizzas.json"

# ---------- Helpers ----------


def read_orders():
    """Read all orders from local JSON file"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def write_orders(data):
    """Write orders to local JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_next_order_id(orders):
    """Generate next unique orderId"""
    if not orders:
        return 1001
    return max(order["orderId"] for order in orders) + 1


# ---------- CRUD Operations ----------


def create_order(order):
    """Add a new pizza order"""
    orders = read_orders()
    order["orderId"] = get_next_order_id(orders)
    orders.append(order)
    write_orders(orders)
    return order


def update_order(order_id, updated_order):
    """Update an existing order by orderId"""
    orders = read_orders()
    for i, o in enumerate(orders):
        if o["orderId"] == order_id:
            updated_order["orderId"] = order_id  # keep same ID
            orders[i] = updated_order
            write_orders(orders)
            return updated_order
    return None


def delete_order(order_id):
    """Delete an order by orderId"""
    orders = read_orders()
    new_orders = [o for o in orders if o["orderId"] != order_id]
    if len(new_orders) != len(orders):  # means something was deleted
        write_orders(new_orders)
        return {"orderId": order_id, "status": "deleted"}
    return {"orderId": order_id, "status": "not found"}


def get_order(order_id):
    """Retrieve a specific order"""
    orders = read_orders()
    for o in orders:
        if o["orderId"] == order_id:
            return o
    return None


def list_orders():
    """Return all orders"""
    return read_orders()


# ---------- Menu ----------


def get_menu():
    return [
        {
            "name": "Margherita",
            "sizes": {"Small": 7.50, "Medium": 9.50, "Large": 11.50},
        },
        {
            "name": "Pepperoni",
            "sizes": {"Small": 8.00, "Medium": 10.00, "Large": 12.00},
        },
        {"name": "Veggie", "sizes": {"Small": 7.75, "Medium": 9.75, "Large": 11.75}},
        {
            "name": "BBQ Chicken",
            "sizes": {"Small": 8.50, "Medium": 10.50, "Large": 12.50},
        },
        {"name": "Hawaiian", "sizes": {"Small": 8.25, "Medium": 10.25, "Large": 12.25}},
    ]
