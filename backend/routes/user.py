from datetime import datetime, timezone, timedelta
from typing import Optional

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import get_db, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from database.db_errors import integrity_error_to_http
from models.user import User
from schemas.user import Token, UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

# tokenUrl es relativo a la base de la API: la ruta real es /users/token
# (por el prefix del router), así que tiene que coincidir exactamente
# o el botón "Authorize" de /docs intenta loguear contra la URL equivocada.
oauth2_schema = OAuth2PasswordBearer(tokenUrl="users/token")


def hash_password(password: str) -> str:
    # bcrypt ignora silenciosamente todo lo que pase de 72 bytes;
    # mejor fallar explícito que dejar que el usuario crea que su
    # contraseña completa lo protege cuando en realidad no es así.
    if len(password.encode("utf-8")) > 72:
        raise ValueError("La contraseña no puede superar los 72 bytes")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña en texto plano coincide con el hash almacenado."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def authenticate_user(email: str, password: str, db: Session) -> User | None:
    user_db = db.query(User).filter(User.email == email).first()
    if not user_db:
        return None
    if not verify_password(password, user_db.password):
        return None
    return user_db


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)
    expire += expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")


def get_current_user(
    token: str = Depends(oauth2_schema),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.activo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    # Sin este chequeo, un usuario desactivado sigue operando hasta
    # que su token expire por su cuenta (hasta 10-12hs con la config
    # pensada para turnos).
    if not user.activo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inactivo")

    return user


def check_admin(user: User = Depends(get_current_user)) -> User:
    if user.rol != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tenés el permiso requerido")
    return user


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OAuth2PasswordRequestForm usa 'username' como nombre de campo
    # fijo del estándar, pero acá lo usamos para recibir el email.
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña inválidos")

    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def usuario_actual(usuario: User = Depends(get_current_user)):
    """Le permite a cualquier usuario logueado ver sus propios datos."""
    return usuario


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    datos: UserCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(check_admin),  # solo un admin puede dar de alta vendedores
):
    try:
        password_hash = hash_password(datos.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))

    nuevo_usuario = User(
        nombre=datos.nombre,
        email=datos.email,
        password=password_hash,
        rol=datos.rol.value,
        activo=datos.activo,
    )

    db.add(nuevo_usuario)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise integrity_error_to_http(e, contexto="un usuario")

    db.refresh(nuevo_usuario)
    return nuevo_usuario