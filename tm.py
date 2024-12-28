from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/")
def read_item(item_id: int, other_id: str, q: str , w : float or None=None):
    return {"item_id": item_id, "q": q, "w":w, "OTHERUD": other_id}