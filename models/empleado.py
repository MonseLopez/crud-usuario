from flask_mysqldb import MySQL

class Empleado:
    def __init__(self, mysql):
        self.mysql = mysql

    def obtener_empleados(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM empleados")
        empleados = cursor.fetchall()
        cursor.close()
        return empleados

    def agregar_empleado(self, nombre, apellido, email, puesto, salario):
        cursor = self.mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO empleados (nombre, apellido, email, puesto, salario)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellido, email, puesto, salario))
        self.mysql.connection.commit()
        cursor.close()

    def actualizar_empleado(self, id, nombre, apellido, email, puesto, salario):
        cursor = self.mysql.connection.cursor()
        cursor.execute("""
            UPDATE empleados SET nombre=%s, apellido=%s, email=%s, puesto=%s, salario=%s
            WHERE id=%s
        """, (nombre, apellido, email, puesto, salario, id))
        self.mysql.connection.commit()
        cursor.close()

    def eliminar_empleado(self, id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("DELETE FROM empleados WHERE id = %s", (id,))
        self.mysql.connection.commit()
        cursor.close()
