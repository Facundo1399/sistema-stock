from fastapi import FastAPI

from routes.productos import router as productos_router


app = FastAPI()
app.include_router(productos_router)
