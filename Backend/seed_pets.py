"""
Seeder de mascotas usando Faker.
Las mascotas se asignan al admin (role_id=1) para que queden AVAILABLE directamente.
Ejecutar: python seed_pets.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from faker import Faker
from faker.providers import date_time
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.pet_model import Pet
from app.models.user_model import User

fake = Faker('es_CO')

SPECIES = ['perro', 'gato']

RAZAS = {
    'perro': [
        'Labrador Retriever', 'Golden Retriever', 'Bulldog Francés', 'Beagle',
        'Poodle', 'Chihuahua', 'Rottweiler', 'Boxer', 'Dálmata', 'Shih Tzu',
        'Schnauzer', 'Pitbull', 'Pomerania', 'Husky Siberiano', 'Criollo',
    ],
    'gato': [
        'Siamés', 'Persa', 'Maine Coon', 'Ragdoll', 'Bengalí',
        'Sphynx', 'Abisinio', 'Birmano', 'Scottish Fold', 'Criollo',
    ],
}

NOMBRES = {
    'perro': [
        'Max', 'Rocky', 'Toby', 'Buddy', 'Charlie', 'Cooper', 'Duke', 'Bear',
        'Zeus', 'Apollo', 'Bruno', 'Thor', 'Koda', 'Rex', 'Simba', 'Loki',
        'Luna', 'Bella', 'Daisy', 'Coco', 'Nala', 'Canela', 'Perla', 'Nina',
    ],
    'gato': [
        'Misu', 'Pelusa', 'Nube', 'Mochi', 'Salem', 'Oreo', 'Gatito', 'Felix',
        'Whiskers', 'Mittens', 'Shadow', 'Midnight', 'Leo', 'Milo', 'Oliver',
        'Luna', 'Cleo', 'Nala', 'Zoe', 'Kitty',
    ],
}

DESCRIPCIONES = [
    "Muy juguetón y cariñoso, se lleva bien con niños y otros animales.",
    "Tranquilo y apacible, perfecto para apartamentos. Le encanta dormir en lugares cálidos.",
    "Activo y leal, necesita ejercicio diario. Ideal para personas que disfrutan del aire libre.",
    "Tímido al principio pero muy afectuoso una vez que te conoce.",
    "Energético y curioso, le fascina explorar su entorno.",
    "Sociable y amigable con todos, nunca ha mostrado agresividad.",
    "Muy inteligente y fácil de entrenar, aprende trucos rápidamente.",
    "Le encanta la compañía humana, sufre si se queda solo por mucho tiempo.",
    "Independiente pero cariñoso a su manera. Ideal para hogares tranquilos.",
    "Rescatado de la calle, ya está vacunado y desparasitado. Busca un hogar con amor.",
    "Ama los abrazos y las caricias. Se adapta bien a cualquier ambiente.",
    "Muy curioso y juguetón, siempre encuentra la manera de entretenerse.",
    "Protector y noble, excelente compañero para toda la familia.",
    "Dócil y obediente, ya tiene entrenamiento básico.",
    "Lleno de energía por las mañanas, pero tranquilo en las tardes.",
]

IMAGES = {
    'perro': [
        'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400',
        'https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400',
        'https://images.unsplash.com/photo-1596492784531-6e6eb5ea9993?w=400',
        'https://images.unsplash.com/photo-1601979031925-424e53b6caaa?w=400',
        'https://images.unsplash.com/photo-1534361960057-19f4434a825d?w=400',
        'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=400',
        'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=400',
        'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=400',
    ],
    'gato': [
        'https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400',
        'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400',
        'https://images.unsplash.com/photo-1529778873920-4da4926a72c2?w=400',
        'https://images.unsplash.com/photo-1495360010541-f48722b34f7d?w=400',
        'https://images.unsplash.com/photo-1518791841217-8f162f1912da?w=400',
        'https://images.unsplash.com/photo-1561948955-570b270e7c36?w=400',
        'https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400',
    ],
}

def random_birth_date() -> datetime:
    days = random.randint(30, 365 * 12)
    return datetime.utcnow() - timedelta(days=days)

def seed_pets(db: Session, count: int = 45):
    admin = db.query(User).filter(User.role_id == 1, User.deleted_at == None).first()
    if not admin:
        print("ERROR: No se encontró un usuario admin (role_id=1). Ejecuta primero el seeder de admin.")
        return

    print(f"Usando admin: {admin.name} {admin.last_name} (id={admin.id})")

    used_names = set()
    created = 0

    while created < count:
        species = random.choice(SPECIES)
        raza = random.choice(RAZAS[species])
        gender = random.choice(['macho', 'hembra'])

        # Nombre único
        nombre_pool = NOMBRES[species].copy()
        random.shuffle(nombre_pool)
        nombre = None
        for n in nombre_pool:
            candidate = f"{n} {created + 1}"
            if candidate not in used_names:
                nombre = candidate
                used_names.add(candidate)
                break
        if not nombre:
            nombre = f"{species.capitalize()} {fake.first_name()} {created + 1}"

        pet = Pet(
            publisher_id=admin.id,
            name=nombre,
            species=species,
            race=raza,
            birth_date=random_birth_date(),
            gender=gender,
            description=random.choice(DESCRIPCIONES),
            image_url=random.choice(IMAGES[species]),
            status='AVAILABLE',
            modalidad='sede',
            telefono_contacto=None,
            gps_status='none',
        )
        db.add(pet)
        created += 1

    db.commit()
    print(f"✅ {created} mascotas creadas exitosamente.")

if __name__ == '__main__':
    db: Session = next(get_db())
    try:
        seed_pets(db, count=45)
    finally:
        db.close()
