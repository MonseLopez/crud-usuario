from flask import Blueprint, request, jsonify, current_app
import MySQLdb

empleado_routes = Blueprint('empleado_routes', __name__)

@empleado_routes.route('/api/empleados', methods=['GET'])
def obtener_empleados():
    cursor = current_app.extensions['mysql'].connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute("SELECT id, nombre, apellido, email, puesto, salario FROM empleado")
    empleados = cursor.fetchall()
    cursor.close()

    # Acceder a los datos como diccionario usando claves
    empleados_json = [{"id": e['id'], "nombre": e['nombre'], "apellido": e['apellido'], "email": e['email'], "puesto": e['puesto'], "salario": e['salario']} for e in empleados]
    return jsonify(empleados_json)

# Obtener un empleado específico por ID
@empleado_routes.route('/api/empleados/<int:id>', methods=['GET'])
def obtener_empleado(id):
    try:
        print(f"Recibiendo solicitud para obtener el empleado con ID: {id}")

        conexion = current_app.extensions['mysql'].connection
        cursor = conexion.cursor(MySQLdb.cursors.DictCursor)  # 👈 Asegúrate de que el cursor devuelve diccionarios

        consulta = "SELECT id, nombre, apellido, email, puesto, salario FROM empleado WHERE id = %s"
        print(f"Ejecutando consulta: {consulta} con ID {id}")

        cursor.execute(consulta, (id,))
        empleado = cursor.fetchone()

        print(f"Resultado de fetchone(): {empleado}")

        if not empleado:
            print(f"⚠️ No se encontró el empleado con ID {id}")
            return jsonify({"error": "Empleado no encontrado"}), 404

        # ✅ Acceder por nombres de columnas en lugar de índices
        empleado_json = {
            "id": empleado["id"],
            "nombre": empleado["nombre"],
            "apellido": empleado["apellido"],
            "email": empleado["email"],
            "puesto": empleado["puesto"],
            "salario": float(empleado["salario"])  # 👈 Convertir Decimal a float
        }
        
        cursor.close()
        return jsonify(empleado_json)

    except Exception as e:
        print(f"❌ Error crítico al obtener el empleado con ID {id}: {e}")
        return jsonify({"error": str(e)}), 500



# Agregar empleado
@empleado_routes.route('/api/empleados', methods=['POST'])
def agregar_empleado():
    datos = request.json
    cursor = current_app.extensions['mysql'].connection.cursor()

    cursor.execute("INSERT INTO empleado (nombre, apellido, email, puesto, salario) VALUES (%s, %s, %s, %s, %s)",
                   (datos["nombre"], datos["apellido"], datos["email"], datos["puesto"], datos["salario"]))
    current_app.extensions['mysql'].connection.commit()
    cursor.close()
    return jsonify({"message": "Empleado agregado correctamente"}), 201

# Editar empleado
@empleado_routes.route('/api/empleados/<int:id>', methods=['PUT'])
def editar_empleado(id):
    datos = request.json
    cursor = current_app.extensions['mysql'].connection.cursor()

    cursor.execute("UPDATE empleado SET nombre=%s, apellido=%s, email=%s, puesto=%s, salario=%s WHERE id=%s",
                   (datos["nombre"], datos["apellido"], datos["email"], datos["puesto"], datos["salario"], id))
    current_app.extensions['mysql'].connection.commit()
    cursor.close()
    return jsonify({"message": "Empleado actualizado correctamente"})

# Eliminar empleado
@empleado_routes.route('/api/empleados/<int:id>', methods=['DELETE'])
def eliminar_empleado(id):
    cursor = current_app.extensions['mysql'].connection.cursor()

    cursor.execute("DELETE FROM empleado WHERE id = %s", (id,))
    current_app.extensions['mysql'].connection.commit()
    cursor.close()
    return jsonify({"message": "Empleado eliminado correctamente"})
