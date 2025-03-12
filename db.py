from flask_mysqldb import MySQL
from config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
