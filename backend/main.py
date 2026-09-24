from fastapi import FastAPI

from routes.detalles import router as detalles_router
from routes.movimientos import router as movimientos_router
from routes.productos import router as productos_router
from routes.proveedores import router as proveedores_router
from routes.user import router as user_router
from routes.ventas import router as ventas_router


app = FastAPI()
app.include_router(productos_router)
app.include_router(proveedores_router)
app.include_router(movimientos_router)
app.include_router(ventas_router)
app.include_router(detalles_router)
app.include_router(user_router)
