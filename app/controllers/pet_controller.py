import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.db_config import get_db_connection
from app.models.pet_model import PetBase


class PetController:

    def create_pet(self, pet: PetBase):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO mascotas (nombre, especie, edad, descripcion, imagen, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    pet.nombre,
                    pet.especie,
                    pet.edad,
                    pet.descripcion,
                    pet.imagen,
                    pet.user_id
                )
            )

            conn.commit()
            return {"resultado": "Mascota creada"}

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            conn.close()


    def get_pet(self, pet_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM mascotas WHERE pet_id = %s", (pet_id,))
            result = cursor.fetchone()

            if result:
                content = {
                    "pet_id": result[0],
                    "nombre": result[1],
                    "especie": result[2],
                    "edad": result[3],
                    "descripcion": result[4],
                    "imagen": result[5],
                    "user_id": result[6]
                }

                return jsonable_encoder(content)

            else:
                raise HTTPException(status_code=404, detail="Mascota no encontrada")

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            conn.close()


    def get_pets(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM mascotas")
            result = cursor.fetchall()

            payload = []

            for data in result:
                content = {
                    "pet_id": data[0],
                    "nombre": data[1],
                    "especie": data[2],
                    "edad": data[3],
                    "descripcion": data[4],
                    "imagen": data[5],
                    "user_id": data[6]
                }
                payload.append(content)

            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No pets found")

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            conn.close()


    def update_pet(self, pet_id: int, pet: PetBase):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE mascotas
                SET nombre=%s, especie=%s, edad=%s, descripcion=%s, imagen=%s, user_id=%s
                WHERE pet_id=%s
                """,
                (
                    pet.nombre,
                    pet.especie,
                    pet.edad,
                    pet.descripcion,
                    pet.imagen,
                    pet.user_id,
                    pet_id
                )
            )

            conn.commit()
            return {"resultado": "Mascota actualizada"}

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            conn.close()


    def delete_pet(self, pet_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM mascotas WHERE pet_id = %s", (pet_id,))
            conn.commit()

            return {"resultado": "Mascota eliminada"}

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            conn.close()
