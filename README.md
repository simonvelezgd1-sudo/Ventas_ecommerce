E-Commerce Data Automation
Descripción del Proyecto
Este proyecto es un sistema de automatización desarrollado en Python para el procesamiento, limpieza e integración de datos transaccionales de comercio electrónico hacia una base de datos PostgreSQL. Su objetivo es asegurar la integridad de los datos, estandarizar los registros y automatizar la carga de información en un entorno relacional para optimizar su posterior análisis.

Arquitectura del Proyecto
El repositorio implementa una estructura modular para separar la lógica de negocio, la configuración y el manejo de datos:
Ventas_ecommerce/
1.data
2.raw/                # Archivos de datos originales sin procesar
3.processed/          # Datos limpios listos para inserción



 sql/
 creacion_tablas.sql # Esquemas de la base de datos
 consultas.sql       # Consultas SQL para validación y análisis
 
src/
main.py             # Orquestador principal del proceso
conexion_bd.py      # Configuración y manejo de la conexión a PostgreSQL
automatizacion.py   # Lógica de extracción, transformación y carga (ETL)

.env                    # Variables de entorno
.gitignore              # Reglas de exclusión para Git
 requirements.txt        # Dependencias del proyecto
README.md               # Documentación del proyecto
