"""Archivo principal de FastAPI."""

from fastapi import FastAPI



from .rutas import libros
app = FastAPI(
    title="API Biblioteca Escolar",
    description="Primera etapa: CRUD de una sola tabla",
    version="1.0.0",
)

app.include_router(libros.router)


@app.get("/", tags=["Estado"])
def inicio():
    return {"estado": "ok", "mensaje": "La API esta funcionando"}

