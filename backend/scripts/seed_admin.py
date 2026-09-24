# seed_admin.py — correr una sola vez con: python seed_admin.py
from config import SessionLocal
from models.user import User
from routes.users import hash_password  # o donde hayas dejado la función

db = SessionLocal()
admin = User(
    nombre="Admin",
    email="admin@tukiosko.com",
    password=hash_password("una-contraseña-fuerte-temporal"),
    rol="admin",
    activo=True,
)
db.add(admin)
db.commit()
db.close()
print("Admin creado.")