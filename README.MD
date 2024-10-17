
# Proyecto de Web Scraping con Selenium

Este proyecto utiliza Selenium para realizar web scraping en el sitio web de CBC Worldwide, extrayendo información sobre propiedades industriales disponibles en el mercado de arrendamiento en Estados Unidos.

## Descripción

El script de Python navega por el sitio web, recopila información relevante sobre propiedades (como nombre, precio, dirección y enlace) y almacena los datos en una base de datos SQLite. También se implementa un sistema de paginación para recorrer múltiples páginas de resultados.

## Requisitos

- Python 3.x
- Selenium
- SQLite
- Un entorno de desarrollo compatible (se recomienda utilizar un entorno virtual)

## Estructura del Proyecto

```
.
├── app
│   ├── Dockerfile
│   ├── WebScraping.py
│   ├── propiedades.db
│   ├── requirements.txt
│   └── start.sh
├── README.md
└── docker-compose.yml
```

## Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Ejecutar el script de scraping**:

   ```bash
   python3 WebScraping.py
   ```

2. **Ver los datos almacenados en la base de datos**:
   Puedes utilizar un cliente SQLite para consultar los datos en `propiedades.db`:

    ```bash
   sqlite3 propiedades.db "SELECT * FROM propiedades;"
   ```

   ### Ver los datos desde Docker

   Para acceder a la base de datos SQLite desde dentro del contenedor Docker:

   1. **Iniciar el contenedor**:

   ```bash
   docker-compose up -d
   ```

   2. **Iniciar una terminal interactiva en el contenedor**:
   En una nueva terminal, ejecuta:

   ```bash
   docker exec -it <NOMBRE_DEL_CONTENEDOR> /bin/bash
   ```

   3. **Consultar los datos en la base de datos**:

   ```bash
   sqlite3 propiedades.db "SELECT * FROM propiedades;"
   ```

## Contribuciones

Si deseas contribuir a este proyecto, siéntete libre de enviar un pull request o abrir un issue para discutir mejoras.
