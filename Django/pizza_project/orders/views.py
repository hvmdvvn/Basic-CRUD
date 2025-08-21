from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .crud import (
    create_order,
    update_order,
    delete_order,
    get_order,
    list_orders,
    get_menu,
)
from .serializers import OrderSerializer

@api_view(["GET"])
def read_orders(request):
    return Response(list_orders())

@api_view(["GET"])
def read_order(request, order_id):
    order = get_order(order_id)
    if order:
        return Response(order)
    return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def add_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        new_order = create_order(serializer.validated_data)
        return Response(new_order, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def modify_order(request, order_id):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        updated = update_order(order_id, serializer.validated_data)
        if updated:
            return Response(updated)
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def remove_order(request, order_id):
    return Response(delete_order(order_id))

@api_view(["GET"])
def menu(request):
    return Response(get_menu())
