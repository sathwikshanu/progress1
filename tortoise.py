#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: sathwik
"""

from typing import List
from fastapi import FastAPI,HTTPException
from model import Todo,TodoIn_Pydantic, Todo_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError,register_tortoise

app = FastAPI()

@app.get("/")
async def read_root():
    return {"hello":"sathwik"}

@app.post("/todo", response_model=Todo_Pydantic)
async def create(todo:TodoIn_Pydantic):
    obj = await Todo.create("todo.dict(exclude_unset=True)")
    return await Todo_Pydantic.from_tortoise_orm(obj)

@app.get("/todo/{id}", response_model=Todo_Pydantic, responses={404:{"model": HTTPNotFoundError}})
async def get_one(id: int):
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=id))

register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules={'models':['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
