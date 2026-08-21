
CREATE DATABASE IF NOT EXISTS biblioteca_db;

USE biblioteca_db;

CREATE TABLE IF NOT EXISTS libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150),
    autor VARCHAR(120),
    genero VARCHAR(60),
    anio_publicacion INT,
    ejemplares INT
);

-- Datos iniciales para probar los endpoints.
INSERT INTO libros (titulo, autor, genero, anio_publicacion, ejemplares)
VALUES
    ('El principito', 'Antoine de Saint-Exupery', 'Narrativa', 1943, 3),
    ('Subterra', 'Baldomero Lillo', 'Cuento', 1904, 2);

