"""
Catálogo de productos.

Usa tres tipos de colecciones de Python, cada una para un propósito
distinto:

- dict  (self._productos): almacenamiento principal, código -> Producto.
  Permite buscar, actualizar y eliminar un producto por su código en
  tiempo constante, sin tener que recorrer toda la colección.

- set   (self._codigos): guarda únicamente los códigos ya registrados.
  Se usa para rechazar productos duplicados de forma inmediata, antes
  de siquiera tocar el diccionario.

- list  (self._historial): guarda, en orden, un registro de cada
  operación realizada sobre el catálogo (agregar/actualizar/eliminar),
  útil para trazabilidad.
"""

from modelos.producto import Producto


class Catalogo:
    def __init__(self):
        self._productos: dict[str, Producto] = {}
        self._codigos: set[str] = set()
        self._historial: list[str] = []

    # ---------- Operaciones CRUD ----------

    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un producto nuevo. Lanza ValueError si el código ya existe."""
        if producto.codigo in self._codigos:
            raise ValueError(f"Ya existe un producto con el código '{producto.codigo}'")

        self._productos[producto.codigo] = producto
        self._codigos.add(producto.codigo)
        self._historial.append(f"AGREGAR: {producto.codigo} - {producto.nombre}")

    def buscar_producto(self, codigo: str) -> Producto | None:
        """Retorna el producto con ese código, o None si no existe."""
        return self._productos.get(codigo)

    def listar_productos(self) -> list[Producto]:
        """Retorna todos los productos del catálogo, como una lista."""
        return list(self._productos.values())

    def actualizar_producto(self, codigo: str, **cambios) -> Producto:
        """
        Actualiza uno o más atributos del producto con ese código.
        Ejemplo: catalogo.actualizar_producto('P001', precio=99.90, stock=5)
        Lanza KeyError si el producto no existe.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise KeyError(f"No existe un producto con el código '{codigo}'")

        for campo, valor in cambios.items():
            if hasattr(producto, campo):
                setattr(producto, campo, valor)

        self._historial.append(f"ACTUALIZAR: {codigo}")
        return producto

    def eliminar_producto(self, codigo: str) -> None:
        """Elimina el producto con ese código. Lanza KeyError si no existe."""
        if codigo not in self._codigos:
            raise KeyError(f"No existe un producto con el código '{codigo}'")

        del self._productos[codigo]
        self._codigos.discard(codigo)
        self._historial.append(f"ELIMINAR: {codigo}")

    # ---------- Consultas auxiliares ----------

    def categorias_disponibles(self) -> list[str]:
        """Retorna, sin repetidos, las categorías presentes en el catálogo."""
        categorias = {producto.categoria for producto in self._productos.values()}
        return sorted(categorias)

    def cantidad_productos(self) -> int:
        return len(self._productos)

    def existe_codigo(self, codigo: str) -> bool:
        return codigo in self._codigos

    def historial(self) -> list[str]:
        """Retorna una copia del historial de operaciones realizadas."""
        return list(self._historial)
