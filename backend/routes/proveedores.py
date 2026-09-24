from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import get_db
from database.db_errors import integrity_error_to_http
from models.proveedores import Proveedore
from models.user import User
from schemas.proveedores import ProveedorResponse, ProveedorCreate, ProveedorUpdate
from routes.user import check_admin, get_current_user

router = APIRouter(prefix="/proveedores", tags=["proveedores"])

@router.get("/", response_model=list[ProveedorResponse])
def get_proveedores(
    db: Session = Depends(get_db),
    _usuario: User = Depends(get_current_user),
):
    return db.query(Proveedore).filter(Proveedore.activo.is_(True)).all()


@router.get("/{proveedor_id}", response_model=ProveedorResponse)
def proveedor_especifico(
    proveedor_id: int,
    db: Session = Depends(get_db),
    _usuario: User = Depends(get_current_user),
):
    especifico = (
        db.query(Proveedore)
        .filter(Proveedore.id == proveedor_id, Proveedore.activo.is_(True))
        .first()
    )

    if especifico is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    return especifico


@router.post("/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
def cargar_proveedor(
    proveedor: ProveedorCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(check_admin),
):
    nuevo_proveedor = Proveedore(**proveedor.model_dump())

    db.add(nuevo_proveedor)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise integrity_error_to_http(e, contexto="un proveedor")
    
    db.refresh(nuevo_proveedor)
    return nuevo_proveedor


@router.put("/{proveedor_id}", response_model=ProveedorResponse)
def mod_proveedor(
    proveedor_id: int,
    proveedor: ProveedorCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(check_admin),
):
    proveedor_mod = db.query(Proveedore).filter(Proveedore.id == proveedor_id).first()

    if proveedor_mod is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    datos_proveedor = proveedor.model_dump()
    for campo, valor in datos_proveedor.items():
        setattr(proveedor_mod, campo, valor)

    try:
        db.commit()
        
    except IntegrityError as e:
        db.rollback()
        raise integrity_error_to_http(e, contexto="el proveedor")

    db.refresh(proveedor_mod)
    return proveedor_mod


@router.patch("/{proveedor_id}", response_model=ProveedorResponse)
def actualizar_parcial(
    proveedor_id: int,
    proveedor: ProveedorUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(check_admin),
):
    proveedor_mod = db.query(Proveedore).filter(Proveedore.id == proveedor_id).first()

    if proveedor_mod is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    datos_proveedor = proveedor.model_dump(exclude_unset=True)
    for campo, valor in datos_proveedor.items():
        setattr(proveedor_mod, campo, valor)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise integrity_error_to_http(e, contexto="el proveedor")
    
    db.refresh(proveedor_mod)
    return proveedor_mod


@router.delete("/{proveedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(check_admin),
):
    proveedor_borrar = db.query(Proveedore).filter(Proveedore.id == proveedor_id).first()

    if proveedor_borrar is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    proveedor_borrar.activo = False
    db.commit()

    return None