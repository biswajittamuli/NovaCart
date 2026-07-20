from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: Decimal
    status: str
    transaction_id: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }