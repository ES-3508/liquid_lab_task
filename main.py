from fastapi import FastAPI
from routes.stock_summary import router as stock_price_router

app = FastAPI()
app.include_router(stock_price_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

