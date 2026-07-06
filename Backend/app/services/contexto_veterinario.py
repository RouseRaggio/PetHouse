from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.models.pet_model import Pet
from app.models.pet_medical_card_model import PetMedicalCard
from app.models.pet_reminder_model import PetReminder


def obtener_contexto_mascota(pet_id: int):

    db: Session = SessionLocal()

    try:

        mascota = (
            db.query(Pet)
            .filter(Pet.id == pet_id)
            .first()
        )

        if not mascota:
            return "No existe información registrada del paciente."

        ficha = (
            db.query(PetMedicalCard)
            .filter(PetMedicalCard.pet_id == pet_id)
            .first()
        )

        recordatorios = (
            db.query(PetReminder)
            .filter(
                PetReminder.pet_id == pet_id,
                PetReminder.deleted_at.is_(None)
            )
            .all()
        )

        contexto = f"""
=========================
PACIENTE
=========================

Nombre:
{mascota.name}

Especie:
{mascota.species}

Raza:
{mascota.race}

Sexo:
{mascota.gender}

Descripción:
{mascota.description or "Sin descripción"}
"""

        if mascota.birth_date:

            contexto += f"""

Fecha de nacimiento:
{mascota.birth_date.strftime('%d/%m/%Y')}
"""

        # =====================================================
        # Ficha médica
        # =====================================================

        if ficha:

            contexto += f"""

=========================
FICHA MÉDICA
=========================

Tipo de sangre:
{ficha.blood_type or "No registrado"}

Alergias:
{ficha.allergies or "Ninguna"}

Condiciones médicas:
{ficha.conditions or "Ninguna"}

Observaciones:
{ficha.observations or "Sin observaciones"}
"""

        # =====================================================
        # Recordatorios
        # =====================================================

        if recordatorios:

            contexto += """

=========================
RECORDATORIOS Y CUIDADOS
=========================
"""

            for r in recordatorios:

                contexto += f"""

--------------------------------

Tipo:
{r.type}

Estado:
{r.status}
"""

                if r.fecha:

                    contexto += f"""

Fecha:
{r.fecha.strftime('%d/%m/%Y')}
"""

                if r.proxima_fecha:

                    contexto += f"""

Próxima fecha:
{r.proxima_fecha.strftime('%d/%m/%Y')}
"""

                if r.notes:

                    contexto += f"""

Notas:
{r.notes}
"""

        return contexto

    finally:
        db.close()