from django.urls import path
from . import views

urlpatterns = [
    path("orders/", views.read_orders),
    path("orders/<int:order_id>/", views.read_order),
    path("orders/add/", views.add_order),
    path("orders/<int:order_id>/update/", views.modify_order),
    path("orders/<int:order_id>/delete/", views.remove_order),
    path("menu/", views.menu),
]
