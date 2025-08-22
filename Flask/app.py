from flask import Flask, request, jsonify
from flasgger import Swagger
from mylib import (
    create_order,
    update_order,
    delete_order,
    get_order,
    list_orders,
    get_menu,
)
from schemas import order_schema, orders_schema

app = Flask(__name__)
swagger = Swagger(app)  # Enable Swagger UI


@app.route("/orders", methods=["GET"])
def read_orders():
    """
    Get all orders
    ---
    responses:
      200:
        description: List of all orders
        schema:
          type: array
          items:
            $ref: '#/definitions/Order'
    """
    orders = list_orders()
    return jsonify(orders_schema.dump(orders))


@app.route("/orders/<int:order_id>", methods=["GET"])
def read_order(order_id):
    """
    Get a single order by ID
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID of the order
    responses:
      200:
        description: Order details
        schema:
          $ref: '#/definitions/Order'
      404:
        description: Order not found
    """
    order = get_order(order_id)
    if order:
        return jsonify(order_schema.dump(order))
    return jsonify({"error": "Order not found"}), 404


@app.route("/orders", methods=["POST"])
def add_order():
    """
    Create a new order
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Order'
    responses:
      200:
        description: Created order
        schema:
          $ref: '#/definitions/Order'
      400:
        description: Validation error
    """
    data = request.get_json()
    errors = order_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    new_order = create_order(data)
    return jsonify(order_schema.dump(new_order))


@app.route("/orders/<int:order_id>", methods=["PUT"])
def modify_order(order_id):
    """
    Update an existing order
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID of the order
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Order'
    responses:
      200:
        description: Updated order
        schema:
          $ref: '#/definitions/Order'
      404:
        description: Order not found
    """
    data = request.get_json()
    errors = order_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    updated = update_order(order_id, data)
    if updated:
        return jsonify(order_schema.dump(updated))
    return jsonify({"error": "Order not found"}), 404


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def remove_order(order_id):
    """
    Delete an order
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID of the order
    responses:
      200:
        description: Order deleted
      404:
        description: Order not found
    """
    result = delete_order(order_id)
    return jsonify(result)


@app.route("/menu", methods=["GET"])
def menu():
    """
    Get menu items
    ---
    responses:
      200:
        description: Menu
        schema:
          type: array
          items:
            type: string
    """
    return jsonify(get_menu())


# Define schema for Swagger docs
swagger.template = {
    "definitions": {
        "Order": {
            "type": "object",
            "properties": {
                "customer": {"type": "string"},
                "address": {"type": "string"},
                "items": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["customer", "address", "items"]
        }
    }
}


if __name__ == "__main__":
    app.run(debug=True, port=8000)
