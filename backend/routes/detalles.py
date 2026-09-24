from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config import get_db
from models.detalles import VentasDetalles
from models.user import User
from schemas.detalles import VentaDetalleResponse
from routes.user import get_current_user

router = APIRouter(prefix="/ventas-detalles", tags=["ventas-detalles"])


@router.get("/", response_model=list[VentaDetalleResponse])
def listar_detalles(
	db: Session = Depends(get_db),
	_usuario: User = Depends(get_current_user),
):
	return db.query(VentasDetalles).order_by(VentasDetalles.id.desc()).all()


@router.get("/venta/{venta_id}", response_model=list[VentaDetalleResponse])
def listar_detalles_venta(
	venta_id: int,
	db: Session = Depends(get_db),
	_usuario: User = Depends(get_current_user),
):
	detalles = (
		db.query(VentasDetalles)
		.filter(VentasDetalles.venta_id == venta_id)
		.order_by(VentasDetalles.id)
		.all()
	)

	if not detalles:
		raise HTTPException(status_code=404, detail="Detalles de venta no encontrados")

	return detalles


@router.get("/{detalle_id}", response_model=VentaDetalleResponse)
def obtener_detalle(
	detalle_id: int,
	db: Session = Depends(get_db),
	_usuario: User = Depends(get_current_user),
):
	detalle = db.query(VentasDetalles).filter(VentasDetalles.id == detalle_id).first()

	if detalle is None:
		raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")

	return detalle
