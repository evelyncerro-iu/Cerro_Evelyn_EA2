"""Pruebas unitarias para validar el funcionamiento del extractor de datos."""

import pytest
from modulos.extractor_datos import ExtractorDiosaBq


@pytest.fixture
def fragmento_html_simulado() -> str:
    """Proporciona un fragmento de HTML con estructura identica a Diosa Bq."""
    return """
    <html>
        <body>
            <div class="card__content">
                <h3 class="card__heading">LABIAL MATTE ROJO GLAMOUR</h3>
                <span class="price-item">$25,000 COP</span>
            </div>
            <div class="card__content">
                <h3 class="card__heading">ILUMINADOR EN POLVO SHINE</h3>
                <span class="price-item">$18,500 COP</span>
            </div>
            <div class="card__content">
                <span class="elemento-invalido">Sin datos requeridos</span>
            </div>
        </body>
    </html>
    """


def test_extraccion_desde_html_exitoso(fragmento_html_simulado: str) -> None:
    """Verifica que el extractor procese adecuadamente las etiquetas esperadas."""
    extractor_objeto = ExtractorDiosaBq()
    productos_obtenidos = extractor_objeto.extraer_desde_html(
        fragmento_html_simulado,
        limite_productos=5
    )

    assert len(productos_obtenidos) == 2
    primer_producto = productos_obtenidos[0]
    assert primer_producto["titulo_crudo"] == "LABIAL MATTE ROJO GLAMOUR"
    assert primer_producto["precio_crudo"] == "$25,000 COP"
    assert primer_producto["estado_extraccion"] == "exitoso"


def test_extraccion_con_limite_de_productos(fragmento_html_simulado: str) -> None:
    """Comprueba que el limite de productos funcione con precision."""
    extractor_objeto = ExtractorDiosaBq()
    productos_obtenidos = extractor_objeto.extraer_desde_html(
        fragmento_html_simulado,
        limite_productos=1
    )

    assert len(productos_obtenidos) == 1
    assert productos_obtenidos[0]["titulo_crudo"] == "LABIAL MATTE ROJO GLAMOUR"


def test_extraccion_html_vacio() -> None:
    """Verifica el comportamiento cuando se suministra HTML sin tarjetas validas."""
    extractor_objeto = ExtractorDiosaBq()
    productos_obtenidos = extractor_objeto.extraer_desde_html(
        "<div>Sin tarjetas validas</div>",
        limite_productos=5
    )

    assert len(productos_obtenidos) == 0
