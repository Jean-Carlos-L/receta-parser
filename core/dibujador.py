"""
Dibujante de arboles sintacticos usando matplotlib.

Exporta una unica funcion: dibujar_arbol(nodo, ax, x, y, ancho_total)
"""


def _contar_hojas(nodo):
    """Devuelve cuantas hojas (terminales) cuelgan de este nodo."""
    if nodo.valor is not None:
        return 1
    return sum(_contar_hojas(h) for h in nodo.hijos)


def _dibujar_rec(nodo, ax, x, y, dx, dy, ancho_total):
    """Dibuja recursivamente el arbol."""
    etiqueta = nodo.etiqueta if not nodo.valor else f"{nodo.etiqueta}\n'{nodo.valor}'"

    if nodo.hijos:
        # Nodo interno: dibujar hijos primero
        hijos_hojas = [_contar_hojas(h) for h in nodo.hijos]
        total_hojas = sum(hijos_hojas)
        x_actual = x - ancho_total / 2

        for hijo, nh in zip(nodo.hijos, hijos_hojas):
            ancho_hijo = nh / total_hojas * ancho_total if total_hojas else 0
            x_hijo = x_actual + ancho_hijo / 2
            y_hijo = y - dy

            ax.plot([x, x_hijo], [y - 0.05, y_hijo + 0.05], color='gray', lw=1.0)

            _dibujar_rec(hijo, ax, x_hijo, y_hijo, dx, dy, ancho_hijo)

            x_actual += ancho_hijo

    ax.text(x, y, etiqueta, ha='center', va='center',
            fontsize=8, bbox=dict(boxstyle='round,pad=0.3', fc='lightyellow', ec='gray', lw=0.8))


def dibujar_arbol(nodo, ax, x, y, ancho_total):
    """Dibuja el arbol sintactico completo sobre el eje *ax*.

    Parametros
    ----------
    nodo : Nodo
        Raiz del arbol a dibujar.
    ax : matplotlib.axes.Axes
        Eje sobre el que se dibuja.
    x, y : float
        Coordenadas de la raiz.
    ancho_total : float
        Espacio horizontal total disponible (en unidades del eje).
    """
    if nodo is None:
        return
    _dibujar_rec(nodo, ax, x, y, 0.8, 0.7, ancho_total)
