from rest_framework import serializers

class OrderItemSerializer(serializers.Serializer):
    pizza = serializers.CharField()
    size = serializers.CharField()
    quantity = serializers.IntegerField()
    extraToppings = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )

class OrderSerializer(serializers.Serializer):
    orderId = serializers.IntegerField(required=False)
    customer = serializers.CharField()
    address = serializers.CharField()
    items = OrderItemSerializer(many=True)
    total = serializers.FloatField()
    status = serializers.CharField()
