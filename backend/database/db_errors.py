from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


def integrity_error_to_http(exc: IntegrityError, contexto: str = "el registro"):
    mensaje = str(exc.orig).lower()

    if "duplicate" in mensaje or "unique" in mensaje:
        detail = f"Ya existe {contexto} con ese valor."
    elif "foreign key" in mensaje or "constraint" in mensaje:
        detail = "La referencia indicada no existe o está asociada a otra entidad."
    else:
        detail = f"No se pudo guardar {contexto} por un conflicto de datos."

    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
