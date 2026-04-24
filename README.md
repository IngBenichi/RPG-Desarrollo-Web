# API REST RPG - Gestión de Personajes y Batallas

Proyecto Backend desarrollado con FastAPI para gestionar personajes de un juego de rol (RPG) y simular batallas entre ellos, aplicando lógica de negocio basada en estadísticas.

## 1. Objetivo

Implementar una API REST que permita:

- Crear, listar, consultar, actualizar y eliminar personajes.
- Simular enfrentamientos entre dos personajes a partir de sus atributos.
- Persistir la información en base de datos SQLite.

## 2. Tecnologías

- Python 3.12
- FastAPI
- SQLAlchemy
- Uvicorn
- Docker / Docker Compose
- SQLite

## 3. Estructura del Proyecto

```text
.
├── app
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers
│       ├── batallas.py
│       └── personajes.py
├── Dockerfile
├── docker-compose.yml
├── main.py
└── requirements.txt
```

## 4. Modelo de Datos

Cada personaje contiene:

- nombre
- color_piel
- raza
- fuerza (0 a 100)
- agilidad (0 a 100)
- magia (0 a 100)
- conocimiento (0 a 100)

## 5. Lógica de Batalla

Se calcula un puntaje por personaje con la fórmula:

$$
\text{puntaje} = (\text{fuerza}\cdot0.35 + \text{agilidad}\cdot0.25 + \text{magia}\cdot0.25)\cdot\left(1 + \frac{\text{conocimiento}}{100}\cdot0.20\right)
$$

Interpretación:

- Fuerza: daño físico directo.
- Agilidad: evasión y velocidad de reacción.
- Magia: ataques especiales.
- Conocimiento: bono estratégico multiplicador.

Si ambos personajes obtienen el mismo puntaje, se retorna empate (HTTP 400 con detalle).

## 6. Formato de Respuestas

La API usa un envoltorio estándar en respuestas exitosas:

```json
{
  "success": true,
  "message": "Mensaje descriptivo",
  "data": {}
}
```

Errores se devuelven en formato FastAPI estándar:

```json
{
  "detail": "Descripción del error"
}
```

## 7. Endpoints

Base URL local: `http://localhost:8000`

Documentación interactiva:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 7.1 Personajes

- `POST /personajes` - Crear personaje
- `GET /personajes` - Listar personajes
- `GET /personajes/{personaje_id}` - Consultar personaje por ID
- `PUT /personajes/{personaje_id}` - Actualizar personaje
- `DELETE /personajes/{personaje_id}` - Eliminar personaje

### 7.2 Batallas

- `POST /batallas` - Simular batalla entre dos personajes

## 8. Ejemplos de Uso

### Crear personaje

```http
POST /personajes
Content-Type: application/json

{
  "nombre": "Eowyn",
  "color_piel": "blanco",
  "raza": "Humano",
  "fuerza": 78,
  "agilidad": 82,
  "magia": 25,
  "conocimiento": 70
}
```

Respuesta:

```json
{
  "success": true,
  "message": "Personaje 'Eowyn' creado exitosamente con ID 6.",
  "data": {
    "nombre": "Eowyn",
    "color_piel": "blanco",
    "raza": "Humano",
    "fuerza": 78,
    "agilidad": 82,
    "magia": 25,
    "conocimiento": 70,
    "id": 6
  }
}
```

### Simular batalla

```http
POST /batallas
Content-Type: application/json

{
  "id_personaje_1": 1,
  "id_personaje_2": 2
}
```

Respuesta:

```json
{
  "success": true,
  "message": "Batalla completada: 'Aragorn' derrota a 'Legolas'.",
  "data": {
    "ganador": {
      "nombre": "Aragorn",
      "color_piel": "blanco",
      "raza": "Humano",
      "fuerza": 85,
      "agilidad": 70,
      "magia": 20,
      "conocimiento": 75,
      "id": 1
    },
    "perdedor": {
      "nombre": "Legolas",
      "color_piel": "blanco",
      "raza": "Elfo",
      "fuerza": 60,
      "agilidad": 95,
      "magia": 40,
      "conocimiento": 80,
      "id": 2
    },
    "puntaje_ganador": 67.0,
    "puntaje_perdedor": 64.2,
    "diferencia": 2.8,
    "resumen": "Aragorn (Humano) venció a Legolas (Elfo) ..."
  }
}
```

## 9. Ejecución en Entorno Local

1. Crear y activar entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar servidor:

```bash
uvicorn main:app --reload
```

## 10. Ejecución con Docker

Construir y levantar contenedor:

```bash
docker compose up --build -d
```

Detener servicios:

```bash
docker compose down
```

Notas:

- El servicio queda en `http://localhost:8000`.
- La base de datos se almacena en volumen Docker (`db_data`) para persistencia.

## 11. Datos Iniciales

Al iniciar la aplicación por primera vez, se insertan automáticamente personajes base si la tabla está vacía:

- Aragorn
- Legolas
- Gimli
- Gandalf
- Sauron

## 12. Estado del Proyecto

- CRUD de personajes: completado.
- Simulación de batallas: completado.
- Dockerización: completada.
- Modularización del código: completada.
