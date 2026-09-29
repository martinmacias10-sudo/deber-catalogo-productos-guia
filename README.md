# Catálogo de Productos (Colecciones + Interfaz Gráfica)

Proyecto de la actividad **Semanas 5 y 6: Colecciones, Genéricos, Interfaz Gráfica y Manejo de Eventos** — curso Programación Estructurada.

**Autor:** Martín Macías

## Descripción del proyecto

Un catálogo de productos con operaciones CRUD (Crear, Consultar, Actualizar, Eliminar), implementado en dos capas:

1. **Lógica del catálogo** (`catalogo/catalogo.py`), que usa tres tipos de colecciones de Python, cada una para un propósito distinto:
   - **`dict`** — almacenamiento principal (`código -> Producto`), para buscar/actualizar/eliminar un producto de forma inmediata por su código.
   - **`set`** — guarda los códigos ya registrados, para rechazar productos duplicados.
   - **`list`** — guarda el historial de operaciones realizadas sobre el catálogo, y también se usa para devolver los productos listados.

2. **Interfaz gráfica** (`main.py`), hecha con [Flet](https://flet.dev/), que expone las 4 operaciones CRUD mediante un formulario, botones y una tabla, con manejo de eventos, validación de los datos ingresados y mensajes de éxito/error.

## Estructura del proyecto

```
.
├── main.py                  # Interfaz gráfica (Flet) — Semana 6
├── demo.py                  # Prueba en consola de las colecciones — Semana 5
├── modelos/
│   └── producto.py          # Clase Producto
└── catalogo/
    └── catalogo.py          # Clase Catalogo (dict + set + list, CRUD)
```

## Requisitos

- Python 3.10 o superior
- [Flet](https://flet.dev/) para la interfaz gráfica

## Instalación

```bash
pip install flet
```

## Cómo ejecutar

**Probar la lógica del catálogo por consola** (sin interfaz gráfica):

```bash
python demo.py
```

**Abrir la interfaz gráfica:**

```bash
python main.py
```

Esto abre una ventana con el catálogo de productos ya cargado con algunos productos de ejemplo. Desde ahí se puede:

- **Agregar** un producto nuevo llenando el formulario y presionando "Agregar".
- **Buscar** un producto escribiendo su código y presionando "Buscar".
- **Actualizar** un producto: hacer clic en su fila de la tabla (esto carga sus datos en el formulario), cambiar los valores deseados y presionar "Actualizar".
- **Eliminar** un producto: hacer clic en su fila y presionar "Eliminar".

La aplicación valida que el código, nombre y categoría no estén vacíos, que el precio sea un número mayor a 0, y que el stock sea un número entero no negativo, mostrando un mensaje de error en rojo si algo no es válido, o un mensaje de éxito en verde cuando la operación se completa.
