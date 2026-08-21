"""Conexion con la base de datos MySQL."""

import os

import pymysql.cursors
from dotenv import load_dotenv


load_dotenv()


def get_conexion():
    """Abre una conexion nueva con MySQL."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database=os.getenv("DB_NAME", "biblioteca_db"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

