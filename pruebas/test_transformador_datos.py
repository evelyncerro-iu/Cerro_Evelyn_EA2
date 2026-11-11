"""Pruebas unitarias para el transformador y exportador de productos."""

import json
import os
from modulos.transformador_datos import TransformadorProductos


def test_limpiar_texto_elimina_espacios_sobrantes() -> None:
    """Verifica que los espacios multiples sean normalizados."""
    transformador = TransformadorProductos()
    texto_sucio = "   ESPEJO   IPAD    NEGRO   GRANDE  \n\t "
    texto_resultado = transformador.limpiar_texto(texto_sucio)

    assert texto_resultado == "ESPEJO IPAD NEGRO GRANDE"


def test_limpiar_precio_numerico_formato_cop() -> None:
    """Verifica la conversion de cadena de precio a float."""
    transformador = TransformadorProductos()
    assert transformador.limpiar_precio_numerico("$17,000 COP") == 17000.0
    assert transformador.limpiar_precio_numerico("$9.500 COP") == 9500.0
    assert transformador.limpiar_precio_numerico("Texto sin digitos") is None
    assert transformador.limpiar_precio_numerico("") is None


def test_estructurar_producto_completo() -> None:
    """Verifica la normalizacion de un registro de producto."""
    transformador = TransformadorProductos()
    registro_entrada = {
        "titulo_crudo": "  PESTAÑINA ALARGAMIENTO BOX OG  ",
        "precio_crudo": "$20,000 COP",
        "estado_extraccion": "exitoso"
    }

    producto_estructurado = transformador.estructurar_producto(registro_entrada)

    assert producto_estructurado["nombre_producto"] == "PESTAÑINA ALARGAMIENTO BOX OG"
    assert producto_estructurado["precio_numerico"] == 20000.0
    assert producto_estructurado["moneda"] == "COP"
    assert producto_estructurado["disponible"] is True


def test_exportacion_a_json_y_csv(tmp_path: str) -> None:
    """Comprueba la correcta persistencia en disco de archivos JSON y CSV."""
    transformador = TransformadorProductos()
    catalogo_ejemplo = [
        {
            "nombre_producto": "BROCHA PARA BASE",
            "precio_texto": "$15,000 COP",
            "precio_numerico": 15000.0,
            "moneda": "COP",
            "disponible": True
        }
    ]

    ruta_archivo_json = os.path.join(str(tmp_path), "salida_test.json")
    ruta_archivo_csv = os.path.join(str(tmp_path), "salida_test.csv")

    resultado_json = transformador.exportar_a_json(catalogo_ejemplo, ruta_archivo_json)
    resultado_csv = transformador.exportar_a_csv(catalogo_ejemplo, ruta_archivo_csv)

    assert resultado_json is True
    assert resultado_csv is True
    assert os.path.exists(ruta_archivo_json)
    assert os.path.exists(ruta_archivo_csv)

    with open(ruta_archivo_json, mode="r", encoding="utf-8") as archivo_leido:
        datos_cargados = json.load(archivo_leido)
        assert len(datos_cargados) == 1
        assert datos_cargados[0]["nombre_producto"] == "BROCHA PARA BASE"
