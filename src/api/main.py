from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from src.database.connection import (
connect_to_db, get_all_products, get_product_by_id, create_order,
get_all_users, get_user_by_id, create_user, update_product, delete_product_by_id
)
from src.models.user import User
from src.models.product import Product
from src.models.order import Order

app = FastAPI()

def test_api():
    client = TestClient(app)

    #Тест GET /products
    response = client.get("/products")
    assert response.status_code == 200
    print("GET /products: OK")

    #Тест GET /products/{id}
    response = client.get("/products/1")
    assert response.status_code == 200
    print("GET /products/1: OK")

    #Тест PUT /products/{id}
    response = client.put("/products/1", json={'name': 'Ноутбук HP', 'price': 20000, 'quantity': 120})
    assert response.status_code == 200
    print("PUT /products/1: OK")

    # Тест DELETE /products/{id}
    response = client.delete("/products/1")
    assert response.status_code == 200
    print("DELETE /products/1: OK")

    # Тест POST /orders
    response = client.post("/orders", json={"user_id": 1, "product_id": 2, "quantity": 1})
    assert response.status_code == 201
    print("POST /orders: OK")

    # Тест GET /users
    response = client.get("/users")
    assert response.status_code == 200
    print("GET /users: OK")

    # Тест GET /users/{id}
    response = client.get("/users/1")
    assert response.status_code == 200
    print("GET /users/1: OK")

    # Тест POST /users
    response = client.post("/users", json={"name": "Борис", "email": "boris@example.com"})
    assert response.status_code == 201
    print("POST /users: OK")

class OrderCreate(BaseModel):
    user_id : int
    product_id: int
    quantity: int

class UserCreate(BaseModel):
    name : str
    email: str

class ProductUpdate(BaseModel):
    name: str
    price: int
    quantity: int

@app.get("/products", status_code=200)
def get_products(limit: int = 10, offset: int = 0, conn=Depends(connect_to_db)):
    try:
        result = list()
        products = get_all_products(conn, limit, offset)
        if not products:
            raise HTTPException(status_code=404, detail=f"Не найдены товары")
        for product_info in products:
            id, name, price, quantity = product_info
            product = Product(name, price, quantity)
            result.append(product.__dict__)
        return {'status_code': 200, 'detail': result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения всех товаров: {e}")

@app.get("/products/{id}", status_code=200)
def get_products_by_id(id: int, conn=Depends(connect_to_db)):
    try:
        product = get_product_by_id(conn, id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Не найден товар с id={id}")
        id, name, price, quantity = product
        res = Product(name, price, quantity)
        return {'detail': res.__dict__}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения товара по id = {id}: {e}")

@app.put("/products/{id}", status_code=200)
def update_product_by_id(id: int, data: ProductUpdate, conn=Depends(connect_to_db)):
    try:
        updated_product = Product(data.name, data.price, data.quantity)
        is_updated = update_product(conn, data, id)
        if is_updated:
            return updated_product.__dict__
        raise HTTPException(status_code=404, detail=f'Товар с id = {id} не найден!')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления товара по id = {id}: {e}")

@app.delete("/products/{id}", status_code=200)
def delete_product(id: int, conn=Depends(connect_to_db)):
    try:
        is_delete = delete_product_by_id(conn, id)
        # print(is_delete)
        if is_delete:
            return {"msg": f"Товар с id = {id} успешно удален!"}
        raise HTTPException(status_code=404, detail=f'Товар с id = {id} не найден!')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления товара по id = {id}: {e}")

@app.post("/orders", status_code=201)
def create_new_order(data: OrderCreate, conn=Depends(connect_to_db)):
    try:
        new_order = Order(data.user_id, data.product_id, data.quantity)
        is_created = create_order(conn, data.user_id, data.product_id, data.quantity)
        if is_created is True:
            return new_order.__dict__
        raise HTTPException(status_code=400, detail='Не удалось создать заказ')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания заказа: {e}")

@app.get("/users", status_code=200)
def get_users(conn=Depends(connect_to_db)):
    try:
        result = list()
        users = get_all_users(conn)
        if not users:
            raise HTTPException(status_code=404, detail=f"Не найдены пользователи")
        for user_info in users:
            id, name, email = user_info
            user = User(name, email)
            result.append(user.__dict__)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения всех пользователей: {e}")

@app.get("/users/{id}", status_code=200)
def get_users_by_id(id: int, conn=Depends(connect_to_db)):
    try:
        user_db = get_user_by_id(conn, id)
        if not user_db:
            raise HTTPException(status_code=404, detail=f"Не найден пользователь с id={id}")
        id, name, email = user_db
        user = User(name, email)
        return user.__dict__
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения пользователя по id = {id}: {e}")

@app.post("/users", status_code=201)
def create_new_user(data: UserCreate, conn=Depends(connect_to_db)):
    try:
        is_created = create_user(conn, data.name, data.email)
        if is_created is True:
            return {'status_code': 201, 'detail': "Пользователь создан"}
        new_user = User(data.name, data.email)
        return new_user.__dict__
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания пользователя: {e}")
