# README

## Título del Proyecto

Gestor de Inventario y Precios para Productos Veterinarios

## Introducción

Este proyecto consiste en un sistema automatizado para gestionar el inventario y los precios de productos veterinarios. Utiliza una base de datos en Firebase y se integra con la API de OpenAI para una interacción mejorada y funciones de búsqueda avanzadas.

## Instalación

Para instalar y ejecutar este proyecto, siga estos pasos:

1. Clone el repositorio en su máquina local.
2. Asegúrese de tener Python instalado.
3. Instale las dependencias necesarias ejecutando `pip install -r requirements.txt`.

## Uso

Para utilizar el sistema, ejecute el script principal. Puede interactuar con el sistema mediante la API, enviando solicitudes para buscar productos, actualizar existencias y precios.

## Características

- **Búsqueda de Productos**: Permite buscar productos en la base de datos por nombre.
- **Actualización de Existencias**: Actualiza la cantidad de existencias de un producto específico.
- **Actualización de Precios**: Permite cambiar el precio de venta de los productos.

## Dependencias

- Python 3.x
- Requests: Para realizar solicitudes HTTP.
- OpenAI API: Se utiliza para la integración con el asistente de OpenAI.

## Configuración

Configure las variables de entorno para el correcto funcionamiento del sistema:

- `OPENAI_API_KEY`: Clave de API para OpenAI.
- `ASSISTANT_ID`: ID del asistente de OpenAI.
- `DATABASE_URL`: URL de la base de datos Firebase.
