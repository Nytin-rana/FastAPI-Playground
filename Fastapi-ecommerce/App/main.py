from fastapi import FastAPI ,HTTPException ,Query ,Path
from .Service.products import get_all_products
from .Schema.product import Product


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI E-commerce application!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    products = {
        1: {"name": "Laptop", "price": 999.99},
        2: {"name": "Smartphone", "price": 499.99},
        3: {"name": "Headphones", "price": 199.99},
    }
    return products[item_id]

@app.get("/products")
def get_products():
    products = get_all_products()
    return products


@app.get("/product")
def list_products(
    name: str = Query(
        default =None,
        min_length=1,
        max_length=50,
        description="Filter products by name",
    ),
    sort_by_price: bool = Query(
        default=False,
        description="Sort products by price",),
    order: str = Query(
        default="asc",
        description="Order of sorting: 'asc' for ascending, 'desc' for descending"),  

    limit: int = Query(
        default=10,
        ge=1,
        le=100, 
        description="Limit the number of products returned"),      
    offset: int = Query(
        default=0,
        ge=0,
        le=1000,
        description="Offset for pagination"),      
):
    products = get_all_products()
    if name:
        needle = name.strip().lower()
        products = [product for product in products if needle in product.get("name", " ").lower()]

    if not products:
        raise HTTPException(status_code=404, detail=f"No products found with the specified name: {name}")

    if sort_by_price:
        products.sort(key=lambda p: p.get("price", 0), reverse=(order == "desc"))

    total_products = len(products) 
    products = products[offset:offset + limit]  # Apply pagination
    return {"total_products": total_products, "products": products}

@app.get("/product/{product_id}")
def get_product_by_id(product_id: str = Path(..., min_length=36, max_length=36, description="The ID of the product to retrieve",example="0005a4ea-ce3f-4dd7-bee0-f4ccc70fea6a")):
    products = get_all_products()
    for product in products:
        if product.get("id") == product_id:
            return product
    raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")



@app.post("/products",status_code=201)
def create_product(product : Product):
    return product