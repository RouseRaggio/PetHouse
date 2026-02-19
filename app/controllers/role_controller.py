import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.db_config import get_db_connection
from app.models.role_model import RoleBase


class RoleController:

    def create_role(self, role: RoleBase):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO roles (nombre, descripcion) VALUES (%s, %s)",
                (role.nombre, role.descripcion)
            )

            conn.commit()
            return {"resultado": "Rol creado"}

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            conn.close()


    def get_role(self, role_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM roles WHERE id = %s", (role_id,))
            result = cursor.fetchone()

            if result:
                content = {
                    "id": result[0],
                    "nombre": result[1],
                    "descripcion": result[2]
                }

                json_data = jsonable_encoder(content)
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Role not found")

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            conn.close()


    def get_roles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM roles")
            result = cursor.fetchall()

            payload = []

            for data in result:
                content = {
                    "id": data[0],
                    "nombre": data[1],
                    "descripcion": data[2]
                }
                payload.append(content)

            json_data = jsonable_encoder(payload)

            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="No roles found")

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            conn.close()


    def update_role(self, role_id: int, role: Role):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE roles SET nombre=%s, descripcion=%s WHERE id=%s",
                (role.nombre, role.descripcion, role_id)
            )

            conn.commit()
            return {"resultado": "Rol actualizado"}

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            conn.close()


    def delete_role(self, role_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM roles WHERE id = %s", (role_id,))

            conn.commit()
            return {"resultado": "Rol eliminado"}

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            conn.close()
