from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"msg": "Hola Mundo!"}

@app.get("/items/{item_id}")
async def item(item_id: int):
    return {"id": item_id}
