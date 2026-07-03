from pydantic import (BaseModel, Field ,AnyUrl, field_validator, model_validator, computed_field)
from typing import Annotated, Literal, Optional, List
from uuid import UUID
from datetime import datetime

class Product(BaseModel):
    id: UUID
    sku: Annotated[str,Field(
        min_length=6,
        max_length=30,
        title="SKU",
        description="Stock Keeping Unit",
        examples=["345-hgd-12d-876h","826-pio-14s-998k"]
        )]
    name: Annotated[str,Field(
        min_length=3,
        max_length=80,
        title="Product Name",
        description="Readable Product Name (3-80 chars)",
        examples=["Xiaomi Model Pro","Realme Model Air"]
        )]
    description: Annotated[
        str,
        Field(max_length=200, description="Short product description"),
    ]

    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="Category like mobiles/laptops/electronics/accessories",
            examples=["mobiles", "laptops"],
        ),
    ]

    brand: Annotated[
        str,
        Field(min_length=2, max_length=40, examples=["Xiaomi", "Apple"]),
    ]

    price: Annotated[float, Field(gt=0, strict=True, description="Base price (INR)")]
    currency: Literal["INR"] = "INR"

    discount_percent: Annotated[
        int,
        Field(ge=0, le=90, description="Discount in percent (0-90)"),
    ] = 0

    stock: Annotated[int, Field(ge=0, description="Available stock (>=0)")]
    is_active: Annotated[bool, Field(description="Is product active?")]

    rating: Annotated[
        float,
        Field(ge=0, le=5, strict=True, description="Rating out of 5"),
    ]
    tags: Annotated[
        Optional[List[str]],
        Field(default=None, max_length=10, description="Up to 10 tags"),
    ]
    image_urls: Annotated[
        List[AnyUrl],
        Field(max_length=1, description="At least 1 image url"),
    ]
    dimensions_cm: DimensionsCM
    seller: Seller
    created_at: datetime
    