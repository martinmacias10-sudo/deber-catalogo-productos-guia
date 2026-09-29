"""
Demostración y prueba manual de las operaciones del catálogo
(Semana 5: colecciones y genéricos).

Prueba: agregar, buscar, listar, actualizar, eliminar, el rechazo de
códigos duplicados, y las consultas auxiliares (categorías, cantidad).
"""

from modelos.producto import Producto
from catalogo.catalogo import Catalogo


def separador(titulo):
    print(f"\n--- {titulo} ---")


def main():
    catalogo = Catalogo()

    separador("Agregando productos")
    productos_iniciales = [
        Producto("P001", "Laptop Lenovo", 750.00, "Electrónica", 10),
        Producto("P002", "Mouse inalámbrico", 15.50, "Electrónica", 50),
        Producto("P003", "Escritorio", 120.00, "Muebles", 8),
        Producto("P004", "Silla ergonómica", 95.00, "Muebles", 12),
        Producto("P005", "Teclado mecánico", 45.00, "Electrónica", 25),
    ]
    for producto in productos_iniciales:
        catalogo.agregar_producto(producto)
        print(f"Agregado: {producto}")

    print(f"\nTotal de productos: {catalogo.cantidad_productos()}")

    separador("Intentando agregar un código duplicado (debe fallar)")
    try:
        catalogo.agregar_producto(Producto("P001", "Otro producto", 10.0, "Otros", 1))
        print("ERROR: no debería haber permitido el duplicado")
    except ValueError as e:
        print(f"Rechazado correctamente: {e}")

    separador("Buscando un producto existente")
    encontrado = catalogo.buscar_producto("P003")
    print(f"Encontrado: {encontrado}")

    separador("Buscando un producto que no existe")
    no_encontrado = catalogo.buscar_producto("P999")
    print(f"Resultado: {no_encontrado}")

    separador("Listando todos los productos")
    for p in catalogo.listar_productos():
        print(p)

    separador("Actualizando un producto (precio y stock de P002)")
    catalogo.actualizar_producto("P002", precio=13.99, stock=40)
    print(catalogo.buscar_producto("P002"))

    separador("Intentando actualizar un producto que no existe (debe fallar)")
    try:
        catalogo.actualizar_producto("P999", precio=1.0)
        print("ERROR: no debería haber permitido actualizar algo inexistente")
    except KeyError as e:
        print(f"Rechazado correctamente: {e}")

    separador("Eliminando un producto")
    catalogo.eliminar_producto("P004")
    print(f"Total de productos después de eliminar: {catalogo.cantidad_productos()}")
    print("¿Sigue existiendo P004?", catalogo.buscar_producto("P004"))

    separador("Categorías disponibles (sin repetidos, usando set)")
    print(catalogo.categorias_disponibles())

    separador("Historial de operaciones (list)")
    for linea in catalogo.historial():
        print(linea)


if __name__ == "__main__":
    main()
