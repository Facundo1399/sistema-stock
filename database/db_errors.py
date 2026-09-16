from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

# Códigos de error de MySQL (estables, documentados por MySQL/MariaDB):
# https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html
ER_DUP_ENTRY = 1062          # UNIQUE constraint violada (ej: codigo repetido)
ER_NO_REFERENCED_ROW_2 = 1452  # FK: el valor referenciado no existe (ej: proveedor_id inválido)
ER_ROW_IS_REFERENCED_2 = 1451  # FK: no se puede borrar/modificar, hay filas hijas que dependen de esta


def integrity_error_to_http(e: IntegrityError, contexto: str = "el registro") -> HTTPException:
    """
    Traduce un IntegrityError de MySQL a un HTTPException legible,
    basándose en el código de error numérico (e.orig.args[0]) en vez
    de parsear el texto del mensaje, que puede variar según el driver
    o el idioma del servidor.

    e.orig.args suele ser algo como: (1062, "Duplicate entry '...' for key 'productos.codigo'")
    Igual usamos el texto SOLO para saber qué columna/índice fue, no
    para decidir el tipo de error (eso lo da el código numérico).
    """
    orig_args = getattr(e.orig, "args", ())
    codigo_error = orig_args[0] if orig_args else None
    mensaje_original = str(orig_args[1]).lower() if len(orig_args) > 1 else ""

    if codigo_error == ER_DUP_ENTRY:
        if "codigo" in mensaje_original:
            detail = "Ya existe un producto con ese código."
        else:
            detail = f"Ya existe {contexto} con ese valor único."
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    if codigo_error == ER_NO_REFERENCED_ROW_2:
        if "proveedor_id" in mensaje_original:
            detail = "El proveedor indicado no existe."
        else:
            detail = "Una de las referencias indicadas no existe."
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    if codigo_error == ER_ROW_IS_REFERENCED_2:
        detail = f"No se puede eliminar {contexto} porque tiene registros asociados."
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    # Cualquier otro IntegrityError no anticipado
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"No se pudo procesar {contexto} por un conflicto de datos.",
    )