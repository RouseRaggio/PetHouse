from app.config.db_config import get_db_connection
import psycopg2

class PetController:

    def create_pet(self, pet_data):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO mascotas (nombre, especie, edad, descripcion, imagen, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                pet_data["nombre"],
                pet_data["especie"],
                pet_data["edad"],
                pet_data["descripcion"],
                pet_data["imagen"],
                pet_data["user_id"]
            )
        )

        conn.commit()
        conn.close()

        return {"mensaje": "Mascota publicada correctamente"}
    
    def get_pet(self, pet_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM mascotas WHERE id = %s", (pet_id,))
        pet = cursor.fetchone()

        conn.close()

        if pet and pet["imagen"]:
            pet["imagen"] = f"http://localhost:8000/uploads/{pet['imagen']}"

        return pet

    def get_pets(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM mascotas")
        pets = cursor.fetchall()

        conn.close()

        # Construir URL completa de imagen
        for pet in pets:
            if pet["imagen"]:
                pet["imagen"] = f"http://localhost:8000/uploads/{pet['imagen']}"

        return pets


    def update_pet(self, pet_id: int, pet_data, user_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM mascotas WHERE id = %s", (pet_id,))
        pet = cursor.fetchone()

        if not pet:
            conn.close()
            return None

        if pet["user_id"] != user_id:
            conn.close()
            return {"error": "No puedes editar esta mascota"}

        cursor.execute(
            "UPDATE mascotas SET nombre=%s, especie=%s, edad=%s, descripcion=%s WHERE id=%s",
            (
                pet_data["nombre"],
                pet_data["especie"],
                pet_data["edad"],
                pet_data["descripcion"],
                pet_id
            )
        )

        conn.commit()
        conn.close()

        return {"mensaje": "Mascota actualizada correctamente"}

    def delete_pet(self, pet_id: int, user_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM mascotas WHERE id = %s", (pet_id,))
        pet = cursor.fetchone()

        if not pet:
            conn.close()
            return None

        if pet["user_id"] != user_id:
            conn.close()
            return {"error": "No puedes eliminar esta mascota"}

        cursor.execute("DELETE FROM mascotas WHERE id = %s", (pet_id,))
        conn.commit()
        conn.close()

        return {"mensaje": "Mascota eliminada correctamente"}
