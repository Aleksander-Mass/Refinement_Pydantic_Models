from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import List, Annotated

# Создаем приложение
app = FastAPI()

# Список пользователей
users: List[dict] = []

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# 1. GET запрос для получения всех пользователей
@app.get("/users")
async def get_users() -> List[User]:
    return users

# 2. POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}")
async def add_user(
    username: Annotated[str, Path(min_length=3, max_length=50, description="Имя пользователя")],
    age: Annotated[int, Path(ge=0, le=120, description="Возраст пользователя (от 0 до 120 лет)")]
) -> User:
    new_id = users[-1]['id'] + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user.dict())
    return new_user

# 3. PUT запрос для обновления данных пользователя
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[int, Path(ge=1, description="ID пользователя, который нужно обновить")],
    username: Annotated[str, Path(min_length=3, max_length=50, description="Новое имя пользователя")],
    age: Annotated[int, Path(ge=0, le=120, description="Новый возраст пользователя (от 0 до 120 лет)")]
) -> User:
    for user in users:
        if user['id'] == user_id:
            user['username'] = username
            user['age'] = age
            return User(**user)
    raise HTTPException(status_code=404, detail="User was not found")

# 4. DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(ge=1, description="ID пользователя, который нужно удалить")]
) -> User:
    for index, user in enumerate(users):
        if user['id'] == user_id:
            removed_user = users.pop(index)
            return User(**removed_user)
    raise HTTPException(status_code=404, detail="User was not found")