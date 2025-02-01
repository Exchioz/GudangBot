from pydantic import BaseModel, Field
from typing import Literal

class TextClassification(BaseModel):
    input: str = Field(..., description="Teks dari input")
    context: str = Field(..., description="Kata kunci dari input")
    classification: Literal['item', 'company', 'default'] = Field(
        ...,
        description="Kategori dari input"
    )
