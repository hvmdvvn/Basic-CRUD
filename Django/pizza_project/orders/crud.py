import json, os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../../..", "pizzas.json")

def read_orders():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_orders(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_next_order_id(orders):
    if not orders:
        return 1001
    return max(order["orderId"] for order in orders) + 1

def create_order(order):
    orders = read_orders()
    order["orderId"] = get_next_order_id(orders)
    orders.append(order)
    write_orders(orders)
    return order

def update_order(order_id, updated_order):
    orders = read_orders()
    for i, o in enumerate(orders):
        if o["orderId"] == order_id:
            updated_order["orderId"] = order_id
            orders[i] = updated_order
            write_orders(orders)
            return updated_order
    return None

def delete_order(order_id):
    orders = read_orders()
    new_orders = [o for o in orders if o["orderId"] != order_id]
    if len(new_orders) != len(orders):
        write_orders(new_orders)
        return {"orderId": order_id, "status": "deleted"}
    return {"orderId": order_id, "status": "not found"}

def get_order(order_id):
    for o in read_orders():
        if o["orderId"] == order_id:
            return o
    return None

def list_orders():
    return read_orders()

def get_menu():
    return [
        {"name": "Margherita", "sizes": {"Small": 7.50, "Medium": 9.50, "Large": 11.50}},
        {"name": "Pepperoni", "sizes": {"Small": 8.00, "Medium": 10.00, "Large": 12.00}},
        {"name": "Veggie", "sizes": {"Small": 7.75, "Medium": 9.75, "Large": 11.75}},
        {"name": "BBQ Chicken", "sizes": {"Small": 8.50, "Medium": 10.50, "Large": 12.50}},
        {"name": "Hawaiian", "sizes": {"Small": 8.25, "Medium": 10.25, "Large": 12.25}},
    ]
