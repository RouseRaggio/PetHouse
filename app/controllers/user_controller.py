import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.user_model import User
from fastapi.encoders import jsonable_encoder

class UserController:
         
    def create_user(self, user: User):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre,apellido,edad,usuario,contrasena, rol) VALUES (%s, %s, %s, %s ,%s,%s)", (user.nombre, user.apellido, user.edad, user.usuario, user.contrasena, "user"))
            conn.commit()
            conn.close()
            return {"resultado": "Usuario creado"}
        except mysql.connector.Error as err:
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id':int(result[0]),
                    'nombre':result[1],
                    'apellido':result[2],
                    'edad':int(result[3]),
                    'usuario':result[4],
                    'contrasena':result[5]
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="User not found")  
                
        except mysql.connector.Error as err:
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
        finally:
            conn.close()
       
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id':data[0],
                    'nombre':data[1],
                    'edad':data[2],
                    'usuario':data[3],
                    'contrasena':data[4]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()
      
      
    
    def update_user(self, user_id: int, user: User):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET nombre=%s, apellido=%s, edad=%s, usuario=%s, contrasena=%s WHERE id=%s", 
                           (user.nombre, user.apellido, user.edad, user.usuario, user.contrasena, user_id))
            conn.commit()
            conn.close()
            return {"resultado": "Usuario actualizado"}
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()   

    def delete_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            conn.commit()
            conn.close()
            return {"resultado": "Usuario eliminado"}
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()  
       

##user_controller = UserController()