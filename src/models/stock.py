from dataclasses import dataclass
from typing import Optional

@dataclass
class Stock:
    item: str
    quantity: int
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None