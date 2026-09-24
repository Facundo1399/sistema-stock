from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import get_db
from database.db_errors import integrity_error_to_http
from models.detalles import VentasDetalles
from models.movimientos import MovimientosStock
from models.productos import Productos
from models.user import User
from models.ventas import Ventas
from schemas.ventas import VentaCreate, VentaResponse
from routes.user import get_current_user

router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.get("/", response_model=list[VentaResponse])
def listar_ventas(
	db: Session = Depends(get_db),
	_usuario: User = Depends(get_current_user),
):
	return db.query(Ventas).order_by(Ventas.fecha.desc(), Ventas.id.desc()).all()


@router.get("/{venta_id}", response_model=VentaResponse)
def obtener_venta(
	venta_id: int,
	db: Session = Depends(get_db),
	_usuario: User = Depends(get_current_user),
):
	venta = db.query(Ventas).filter(Ventas.id == venta_id).first()

	if venta is None:
		raise HTTPException(status_code=404, detail="Venta no encontrada")

	return venta


@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(
	venta_data: VentaCreate,
	db: Session = Depends(get_db),
	usuario: User = Depends(get_current_user),
):
	producto_ids = [detalle.producto_id for detalle in venta_data.detalles]
	if len(producto_ids) != len(set(producto_ids)):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="No se puede repetir un producto dentro de la misma venta.",
		)

	venta = Ventas(
		usuario_id=usuario.id,
		metodo_pago=venta_data.metodo_pago,
		total=Decimal("0.00"),
	)
	db.add(venta)
	db.flush()

	total = Decimal("0.00")

	for detalle_data in venta_data.detalles:
		producto = (
			db.query(Productos)
			.filter(Productos.id == detalle_data.producto_id)
			.with_for_update()
			.first()
		)

		if producto is None:
			db.rollback()
			raise HTTPException(status_code=404, detail="Producto no encontrado")

		if not producto.activo:
			db.rollback()
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail=f"El producto '{producto.nombre}' está dado de baja.",
			)

		if producto.cantidad < detalle_data.cantidad:
			db.rollback()
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail=f"Stock insuficiente para el producto '{producto.nombre}'.",
			)

		cantidad_anterior = producto.cantidad
		cantidad_nueva = cantidad_anterior - detalle_data.cantidad
		precio_unitario = producto.precio_venta
		subtotal = precio_unitario * detalle_data.cantidad
		total += subtotal
		producto.cantidad = cantidad_nueva

		detalle = VentasDetalles(
			venta_id=venta.id,
			producto_id=producto.id,
			cantidad=detalle_data.cantidad,
			precio_unitario=precio_unitario,
			subtotal=subtotal,
		)
		movimiento = MovimientosStock(
			producto_id=producto.id,
			tipo="salida",
			cantidad=detalle_data.cantidad,
			cantidad_anterior=cantidad_anterior,
			cantidad_nueva=cantidad_nueva,
			motivo="venta",
			usuario_id=usuario.id,
			referencia_id=venta.id,
		)
		db.add(detalle)
		db.add(movimiento)

	venta.total = total

	try:
		db.commit()
	except IntegrityError as exc:
		db.rollback()
		raise integrity_error_to_http(exc, contexto="la venta")

	db.refresh(venta)
	return venta
