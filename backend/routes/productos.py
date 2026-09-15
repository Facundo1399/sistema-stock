from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import get_db
from models.productos import Productos
from schemas.productos import ProductoResponse, ProductoCreate, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Productos).filter(Productos.activo.is_(True)).all()


@router.get("/{producto_id}", response_model=ProductoResponse)
def producto_especifico(producto_id: int, db: Session = Depends(get_db)):
    especifico = (
        db.query(Productos)
        .filter(Productos.id == producto_id, Productos.activo.is_(True))
        .first()
    )

    if especifico is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return especifico


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def cargar_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    nuevo_producto = Productos(**producto.model_dump())

    db.add(nuevo_producto)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # distinguimos el motivo real del error para dar un mensaje útil
        mensaje = str(e.orig).lower()
        if "codigo" in mensaje:
            detail = "Ya existe un producto con ese código."
        elif "proveedor_id" in mensaje or "foreign key" in mensaje:
            detail = "El proveedor indicado no existe."
        else:
            detail = "No se pudo crear el producto por un conflicto de datos."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    db.refresh(nuevo_producto)
    return nuevo_producto


@router.put("/{producto_id}", response_model=ProductoResponse)
def mod_producto(
    producto_id: int,
    producto: ProductoCreate,
    db: Session = Depends(get_db),
):
    producto_mod = db.query(Productos).filter(Productos.id == producto_id).first()

    if producto_mod is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    datos_producto = producto.model_dump()
    for campo, valor in datos_producto.items():
        setattr(producto_mod, campo, valor)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        mensaje = str(e.orig).lower()
        if "codigo" in mensaje:
            detail = "Ya existe un producto con ese código."
        elif "proveedor_id" in mensaje or "foreign key" in mensaje:
            detail = "El proveedor indicado no existe."
        else:
            detail = "No se pudo actualizar el producto por un conflicto de datos."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    db.refresh(producto_mod)
    return producto_mod


@router.patch("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto_parcial(
    producto_id: int,
    producto: ProductoUpdate,
    db: Session = Depends(get_db),
):
    producto_mod = db.query(Productos).filter(Productos.id == producto_id).first()

    if producto_mod is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    datos_producto = producto.model_dump(exclude_unset=True)
    for campo, valor in datos_producto.items():
        setattr(producto_mod, campo, valor)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        mensaje = str(e.orig).lower()
        if "codigo" in mensaje:
            detail = "Ya existe un producto con ese código."
        elif "proveedor_id" in mensaje or "foreign key" in mensaje:
            detail = "El proveedor indicado no existe."
        else:
            detail = "No se pudo actualizar el producto por un conflicto de datos."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    db.refresh(producto_mod)
    return producto_mod



@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto_borrar = db.query(Productos).filter(Productos.id == producto_id).first()

    if producto_borrar is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto_borrar.activo = False
    db.commit()

    return None