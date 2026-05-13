from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from src.database.connection import (
connect_to_db, get_all_products, get_product_by_id, create_order,
get_all_users, get_user_by_id, create_user
)

app = FastAPI()

class OrderCreate(BaseModel):
    user_id : int
    product_id: int
    quantity: int

class UserCreate(BaseModel):
    name : str
    email: str


@app.get("/products")
def get_products(limit: int = 10, offset: int = 0, conn=Depends(connect_to_db)):
    try:
        products = get_all_products(conn, limit, offset)
        if not products:
            raise HTTPException(status_code=404, detail=f"Не найдены товары")
        return {'status_code': 200, 'detail': products}
    except HTTPException:
        raise
    except Exception as e:
        return f"Ошибка получения всех товаров: {e}"

@app.get("/products/{id}")
def get_products_by_id(id: int, conn=Depends(connect_to_db)):
    try:
        product = get_product_by_id(conn, id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Не найден товар с id={id}")
        return {'status_code': 200, 'detail': product}
    except HTTPException:
        raise
    except Exception as e:
        return f"Ошибка получения товара по id = {id}: {e}"


@app.post("/orders")
def create_new_order(data: OrderCreate, conn=Depends(connect_to_db)):
    try:
        is_created = create_order(conn, data.user_id, data.product_id, data.quantity)
        if is_created is True:
            return {'status_code': 201, 'detail': "Заказ создан"}
        return {"msg": "Не получилось создать заказ"}
    except Exception as e:
        return f"Ошибка создания заказа: {e}"

@app.get("/users")
def get_users(conn=Depends(connect_to_db)):
    try:
        users = get_all_users(conn)
        if not users:
            raise HTTPException(status_code=404, detail=f"Не найдены пользователи")
        return {'status_code': 200, 'detail': users}
    except HTTPException:
        raise
    except Exception as e:
        return f"Ошибка получения всех пользователей: {e}"

@app.get("/users/{id}")
def get_users_by_id(id: int, conn=Depends(connect_to_db)):
    try:
        user = get_user_by_id(conn, id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Не найден пользователь с id={id}")
        return {'status_code': 200, 'detail': user}
    except HTTPException:
        raise
    except Exception as e:
        return f"Ошибка получения пользователя по id = {id}: {e}"

@app.post("/users")
def create_new_user(data: UserCreate, conn=Depends(connect_to_db)):
    try:
        is_created = create_user(conn, data.name, data.email)
        if is_created is True:
            return {'status_code': 201, 'detail': "Пользователь создан"}
        return {"msg": "Не получилось создать пользователя"}
    except Exception as e:
        return f"Ошибка создания пользователя: {e}"