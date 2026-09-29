"""
Interfaz gráfica del catálogo de productos, hecha con Flet.

Implementa las 4 operaciones CRUD (Crear, Consultar, Actualizar,
Eliminar) desde botones, con manejo de eventos, validación de los
datos ingresados y mensajes de éxito/error.
"""

import flet as ft

from modelos.producto import Producto
from catalogo.catalogo import Catalogo


def main(page: ft.Page):
    page.title = "Catálogo de Productos"
    page.padding = 20
    page.scroll = "auto"

    catalogo = Catalogo()

    # ---------- Controles del formulario ----------
    campo_codigo = ft.TextField(label="Código", width=140)
    campo_nombre = ft.TextField(label="Nombre", width=220)
    campo_categoria = ft.TextField(label="Categoría", width=160)
    campo_precio = ft.TextField(label="Precio", width=110)
    campo_stock = ft.TextField(label="Stock", width=90)

    mensaje = ft.Text(value="", size=14)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Stock")),
        ],
        rows=[],
    )

    # ---------- Funciones auxiliares ----------
    def limpiar_campos():
        campo_codigo.value = ""
        campo_codigo.disabled = False
        campo_nombre.value = ""
        campo_categoria.value = ""
        campo_precio.value = ""
        campo_stock.value = ""

    def mostrar_mensaje(texto, es_error=False):
        mensaje.value = texto
        mensaje.color = "red" if es_error else "green"
        page.update()

    def validar_campos():
        if not campo_codigo.value or not campo_nombre.value or not campo_categoria.value:
            return "El código, nombre y categoría son obligatorios."
        try:
            precio = float(campo_precio.value)
            if precio <= 0:
                return "El precio debe ser un número mayor a 0."
        except (TypeError, ValueError):
            return "El precio debe ser un número válido (ej: 19.99)."
        try:
            stock = int(campo_stock.value)
            if stock < 0:
                return "El stock no puede ser negativo."
        except (TypeError, ValueError):
            return "El stock debe ser un número entero (ej: 10)."
        return None

    def refrescar_tabla():
        tabla.rows.clear()
        for producto in catalogo.listar_productos():
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(producto.codigo)),
                        ft.DataCell(ft.Text(producto.nombre)),
                        ft.DataCell(ft.Text(producto.categoria)),
                        ft.DataCell(ft.Text(f"${producto.precio:.2f}")),
                        ft.DataCell(ft.Text(str(producto.stock))),
                    ],
                    on_select_changed=lambda e, cod=producto.codigo: cargar_producto(cod),
                )
            )
        page.update()

    def cargar_producto(codigo):
        """Se ejecuta al hacer clic en una fila de la tabla: carga ese
        producto en el formulario para poder editarlo o eliminarlo."""
        producto = catalogo.buscar_producto(codigo)
        if producto is None:
            return
        campo_codigo.value = producto.codigo
        campo_codigo.disabled = True  # el código no se edita, identifica al producto
        campo_nombre.value = producto.nombre
        campo_categoria.value = producto.categoria
        campo_precio.value = str(producto.precio)
        campo_stock.value = str(producto.stock)
        mostrar_mensaje(f"Producto '{codigo}' cargado. Puedes actualizarlo o eliminarlo.")

    # ---------- Manejadores de eventos (botones) ----------
    def agregar_click(e):
        error = validar_campos()
        if error:
            mostrar_mensaje(error, es_error=True)
            return
        try:
            producto = Producto(
                codigo=campo_codigo.value.strip(),
                nombre=campo_nombre.value.strip(),
                precio=float(campo_precio.value),
                categoria=campo_categoria.value.strip(),
                stock=int(campo_stock.value),
            )
            catalogo.agregar_producto(producto)
            mostrar_mensaje(f"Producto '{producto.nombre}' agregado correctamente.")
            limpiar_campos()
            refrescar_tabla()
        except ValueError as ex:
            mostrar_mensaje(str(ex), es_error=True)

    def actualizar_click(e):
        if not campo_codigo.value:
            mostrar_mensaje("Selecciona un producto de la tabla para actualizar.", es_error=True)
            return
        error = validar_campos()
        if error:
            mostrar_mensaje(error, es_error=True)
            return
        try:
            catalogo.actualizar_producto(
                campo_codigo.value,
                nombre=campo_nombre.value.strip(),
                categoria=campo_categoria.value.strip(),
                precio=float(campo_precio.value),
                stock=int(campo_stock.value),
            )
            mostrar_mensaje("Producto actualizado correctamente.")
            limpiar_campos()
            refrescar_tabla()
        except KeyError as ex:
            mostrar_mensaje(str(ex), es_error=True)

    def eliminar_click(e):
        if not campo_codigo.value:
            mostrar_mensaje("Selecciona un producto de la tabla para eliminar.", es_error=True)
            return
        try:
            catalogo.eliminar_producto(campo_codigo.value)
            mostrar_mensaje("Producto eliminado correctamente.")
            limpiar_campos()
            refrescar_tabla()
        except KeyError as ex:
            mostrar_mensaje(str(ex), es_error=True)

    def limpiar_click(e):
        limpiar_campos()
        mensaje.value = ""
        page.update()

    def buscar_click(e):
        codigo = campo_codigo.value
        if not codigo:
            mostrar_mensaje("Escribe un código para buscar.", es_error=True)
            return
        producto = catalogo.buscar_producto(codigo)
        if producto is None:
            mostrar_mensaje(f"No se encontró ningún producto con el código '{codigo}'.", es_error=True)
        else:
            cargar_producto(codigo)

    # ---------- Construcción de la página ----------
    page.add(
        ft.Text("Catálogo de Productos", size=24, weight="bold"),
        ft.Text("Semana 5 y 6 — Colecciones, Genéricos e Interfaz Gráfica", size=13, italic=True),
        ft.Row([campo_codigo, campo_nombre, campo_categoria, campo_precio, campo_stock], wrap=True),
        ft.Row(
            [
                ft.ElevatedButton("Agregar", on_click=agregar_click),
                ft.ElevatedButton("Buscar", on_click=buscar_click),
                ft.ElevatedButton("Actualizar", on_click=actualizar_click),
                ft.ElevatedButton("Eliminar", on_click=eliminar_click),
                ft.OutlinedButton("Limpiar formulario", on_click=limpiar_click),
            ],
            wrap=True,
        ),
        mensaje,
        ft.Divider(),
        ft.Text("Productos registrados (haz clic en una fila para editarla):", size=14),
        tabla,
    )

    # ---------- Datos de prueba iniciales ----------
    for p in [
        Producto("P001", "Laptop Lenovo", 750.00, "Electrónica", 10),
        Producto("P002", "Mouse inalámbrico", 15.50, "Electrónica", 50),
        Producto("P003", "Escritorio", 120.00, "Muebles", 8),
        Producto("P004", "Silla ergonómica", 95.00, "Muebles", 12),
    ]:
        catalogo.agregar_producto(p)
    refrescar_tabla()


if __name__ == "__main__":
    ft.app(target=main)
