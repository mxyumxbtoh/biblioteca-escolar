<div align="center">

# 📚 Biblioteca Escolar API

### Backend inicial con FastAPI y MySQL

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST-009688?style=flat-square&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Base_de_datos-4479A1?style=flat-square&logo=mysql&logoColor=white)

</div>

Proyecto backend para administrar libros mediante una API REST. Esta version
contiene una sola tabla y servira como punto de partida para construir el
frontend durante las clases.

## Recorrido de los datos

```text
Cliente → FastAPI → consulta SQL → MySQL
Cliente ←   JSON  ← resultado ───← MySQL
```

## Tabla `libros`

| Campo | Tipo | Descripcion |
|---|---|---|
| `id` | `INT` | Identificador autoincremental |
| `titulo` | `VARCHAR(150)` | Titulo del libro |
| `autor` | `VARCHAR(120)` | Nombre del autor |
| `genero` | `VARCHAR(60)` | Genero literario |
| `anio_publicacion` | `INT` | Ano de publicacion |
| `ejemplares` | `INT` | Cantidad disponible |


## Estructura

```text
biblioteca-libros-inicial/
├── backend/
│   ├── connect.py
│   ├── main.py
│   └── rutas/
│       └── libros.py
├── .env.example
├── .gitignore
├── requirements.txt
└── schema.sql
```

## Instalacion

```powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
```

Completar `.env` con la configuracion local de MySQL y ejecutar `schema.sql`
desde DBeaver.

## Ejecutar la API

```bash
uvicorn backend.main:app --reload
```

Documentacion interactiva:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

| Metodo | Endpoint | Operacion |
|---|---|---|
| `GET` | `/libros/` | Listar libros |
| `GET` | `/libros/{id}` | Buscar un libro |
| `POST` | `/libros/` | Crear un libro |
| `PUT` | `/libros/{id}` | Actualizar un libro |
| `DELETE` | `/libros/{id}` | Eliminar un libro |

## JSON de ejemplo

```json
{
  "titulo": "Papelucho",
  "autor": "Marcela Paz",
  "genero": "Infantil",
  "anio_publicacion": 1947,
  "ejemplares": 4
}
```

<div align="center">

Proyecto educativo para el desarrollo de aplicaciones cliente-servidor.

</div>

