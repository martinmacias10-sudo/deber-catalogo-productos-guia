"""Modelo de dominio: representa un producto del catálogo."""


class Producto:
    """Un producto que puede almacenarse en el catálogo."""

    def __init__(self, codigo: str, nombre: str, precio: float, categoria: str, stock: int):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock

    def __str__(self):
        return (f"[{self.codigo}] {self.nombre} - ${self.precio:.2f} "
                f"({self.categoria}) - Stock: {self.stock}")

    def __repr__(self):
        return (f"Producto(codigo={self.codigo!r}, nombre={self.nombre!r}, "
                f"precio={self.precio!r}, categoria={self.categoria!r}, stock={self.stock!r})")
