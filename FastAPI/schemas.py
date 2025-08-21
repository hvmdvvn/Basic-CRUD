from typing import List, Optional
from pydantic import BaseModel

# ---------- Schemas ----------


class OrderItem(BaseModel):
    pizza: str
    size: str
    quantity: int
    extraToppings: Optional[List[str]] = []


class OrderBase(BaseModel):
    customer: str
    address: str
    items: List[OrderItem]
    total: float
    status: str


class OrderCreate(OrderBase):
    """Schema for creating a new order (no orderId yet)"""

    pass


class OrderUpdate(OrderBase):
    """Schema for updating an order"""

    pass


class Order(OrderBase):
    """Schema returned in responses (has ID)"""

    orderId: int
