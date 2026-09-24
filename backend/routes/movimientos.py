from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import get_db
from database.db_errors import integrity_error_to_http
from models.movimientos import MovimientosStock
from models.productos import Productos
from models.user import User
from schemas.movimientos import MovimientoCreate, MovimientoResponse
from routes.user import check_admin, get_current_user

router = APIRouter(prefix="/movimientos-stock", tags=["movimientos-stock"])


@router.get("/", response_model=list[MovimientoResponse])
def mostrar_mov(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    _usuario: User = Depends(get_current_user),
):
    return (
        db.query(MovimientosStock)
        .order_by(MovimientosStock.fecha.desc(), MovimientosStock.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/{movimiento_id}", response_model=MovimientoResponse)
def mov_especifico(
    movimiento_id: int,
    db: Session = Depends(get_db),
    _usuario: User = Depends(get_current_user),
):
    especifico = (
        db.query(MovimientosStock)
        .filter(MovimientosStock.id == movimiento_id)
        .first()
    )

    if especifico is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    return especifico


@router.post("/", response_model=MovimientoResponse, status_code=status.HTTP_201_CREATED)
def crear_movimiento(
    movimiento: MovimientoCreate,
    db: Session = Depends(get_db),
    usuario: User = Depends(check_admin),
):
    if movimiento.tipo in ("entrada", "salida") and movimiento.cantidad <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cantidad debe ser mayor que 0 para entradas y salidas.",
        )

    # with_for_update: bloquea la fila hasta el commit, para que dos
    # movimientos simultáneos del mismo producto no lean el mismo
    # stock inicial y se pisen entre sí.
    producto = (
        db.query(Productos)
        .filter(Productos.id == movimiento.producto_id)
        .with_for_update()
        .first()
    )

    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if not producto.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El producto '{producto.nombre}' está dado de baja.",
        )

    cantidad_anterior = producto.cantidad

    if movimiento.tipo == "entrada":
        cantidad_nueva = cantidad_anterior + movimiento.cantidad
        cantidad_registrada = movimiento.cantidad

    elif movimiento.tipo == "salida":
        if cantidad_anterior < movimiento.cantidad:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La cantidad solicitada supera el stock actual.",
            )
        cantidad_nueva = cantidad_anterior - movimiento.cantidad
        cantidad_registrada = movimiento.cantidad

    else:  
        if movimiento.cantidad == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ajuste no puede ser 0.",
            )

        cantidad_nueva = cantidad_anterior + movimiento.cantidad
        cantidad_registrada = movimiento.cantidad

        if cantidad_nueva < 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El ajuste dejaría el stock en un valor negativo.",
            )

    producto.cantidad = cantidad_nueva

    nuevo_movimiento = MovimientosStock(
        producto_id=movimiento.producto_id,
        tipo=movimiento.tipo,
        cantidad=cantidad_registrada,
        cantidad_anterior=cantidad_anterior,
        cantidad_nueva=cantidad_nueva,
        motivo=movimiento.motivo,
        usuario_id=usuario.id,
        referencia_id=movimiento.referencia_id,
    )

    db.add(nuevo_movimiento)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise integrity_error_to_http(e, contexto="el movimiento")

    db.refresh(nuevo_movimiento)
    return nuevo_movimiento