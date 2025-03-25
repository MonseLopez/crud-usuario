from flask import Flask, render_template
from flask_mysqldb import MySQL
from routes.empleado_routes import empleado_routes

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'gestion_empleados'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Inicializar MySQL
mysql = MySQL(app)
app.extensions['mysql'] = mysql

# Registrar rutas
app.register_blueprint(empleado_routes)

# Ruta de inicio (index)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
