DROP TABLE IF EXISTS Prestamo;
DROP TABLE IF EXISTS Persona;
DROP TABLE IF EXISTS Libro;

CREATE TABLE Persona (
    userid INT PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    dni VARCHAR UNIQUE,
    nacimiento DATE CONSTRAINT mayor_de_edad CHECK (nacimiento < '2001-01-01'),
    suspension BOOLEAN,
    genero VARCHAR (1) CHECK (genero ISNULL OR genero = 'm' OR genero = 'f')
);

CREATE TABLE Libro (
    titulo VARCHAR,
    autor VARCHAR,
    genero CHAR(10),
    ejemplares INT,
    diasPrestamo SMALLINT,
    precio REAL,
    PRIMARY KEY (titulo, autor)
);

CREATE TABLE Prestamo (
    fecha TIMESTAMPTZ,
    fecha_local TIME,
    duracion_maxima INTERVAL,
    titulo VARCHAR,
    autor VARCHAR,
    persona INT,
    PRIMARY KEY (titulo, autor, persona),
    FOREIGN KEY (persona) REFERENCES Persona (userid) MATCH SIMPLE,
    FOREIGN KEY (titulo, autor) REFERENCES Libro (titulo, autor) MATCH SIMPLE
);

