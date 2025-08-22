from marshmallow import Schema, fields, validate


class ItemSchema(Schema):
    pizza = fields.String(required=True)
    size = fields.String(
        required=True,
        validate=validate.OneOf(["Small", "Medium", "Large"])
    )
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    extraToppings = fields.List(fields.String(), required=False)


class OrderSchema(Schema):
    orderId = fields.Int(required=False)  # auto-generated
    customer = fields.String(required=True)
    address = fields.String(required=True)
    items = fields.List(fields.Nested(ItemSchema), required=True)
    total = fields.Float(required=True, validate=validate.Range(min=0))
    status = fields.String(
        required=True,
        validate=validate.OneOf(["Pending", "Preparing", "Delivered", "Cancelled"])
    )


# Instances to use in app.py
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
