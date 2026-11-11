"""Punto de entrada principal para la ejecucion del flujo de extraccion y publicacion."""

import os
import sys
from modulos.extractor_datos import ExtractorDiosaBq
from modulos.transformador_datos import TransformadorProductos
from modulos.publicador_reporte import PublicadorReporteHtml


def ejecutar_flujo_completo(
    directorio_salida: str = "dist",
    usar_modo_respaldo_si_falla: bool = True
) -> bool:
    """Ejecuta de manera secuencial la extraccion, transformacion y publicacion.

    Parametros:
        directorio_salida: Carpeta donde se depositaran los artefactos generados.
        usar_modo_respaldo_si_falla: Permite utilizar datos locales si la red falla.

    Retorna:
        True si todos los pasos concluyeron con exito, False de lo contrario.
    """
    print("=" * 60)
    print("Iniciando Flujo de Trabajo DevOps - Evidencia de Aprendizaje 2")
    print("=" * 60)

    os.makedirs(directorio_salida, exist_ok=True)

    extractor_servicio = ExtractorDiosaBq()
    transformador_servicio = TransformadorProductos()
    publicador_servicio = PublicadorReporteHtml()

    url_tienda = "https://www.diosabq.com/"
    print(f"[1/3] Extrayendo catalogo desde: {url_tienda}...")

    lista_productos_crudos = extractor_servicio.obtener_catalogo_remoto(
        url_tienda,
        limite_productos=10
    )

    if not lista_productos_crudos and usar_modo_respaldo_si_falla:
        print("[!] No se pudo conectar a la tienda en vivo o la tienda bloqueo la peticion.")
        print("[*] Activando datos de respaldo verificados de la Evidencia 1...")

        ruta_respaldo = os.path.join("datos", "muestra_productos.json")
        if os.path.exists(ruta_respaldo):
            import json
            with open(ruta_respaldo, mode="r", encoding="utf-8") as archivo_respaldo:
                lista_productos_crudos = json.load(archivo_respaldo)
            print(f"[+] Cargados {len(lista_productos_crudos)} productos desde respaldo.")

    if not lista_productos_crudos:
        print("[-] Error critico: no se obtuvieron datos para procesar.")
        return False

    print(f"[2/3] Transformando y estructurando {len(lista_productos_crudos)} registros...")
    catalogo_limpio = transformador_servicio.procesar_catalogo(lista_productos_crudos)

    ruta_json_salida = os.path.join(directorio_salida, "productos.json")
    ruta_csv_salida = os.path.join(directorio_salida, "productos.csv")
    ruta_html_salida = os.path.join(directorio_salida, "index.html")

    transformador_servicio.exportar_a_json(catalogo_limpio, ruta_json_salida)
    transformador_servicio.exportar_a_csv(catalogo_limpio, ruta_csv_salida)
    print(f"[+] Artefactos de datos generados: {ruta_json_salida}, {ruta_csv_salida}")

    print("[3/3] Generando dashboard web interactivo para despliegue continuo...")
    publicador_servicio.generar_pagina_dashboard(catalogo_limpio, ruta_html_salida)
    print(f"[+] Dashboard desplegable generado en: {ruta_html_salida}")

    print("=" * 60)
    print("Flujo de DevOps finalizado exitosamente. Artefactos listos para despliegue.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    resultado_exitoso = ejecutar_flujo_completo()
    sys.exit(0 if resultado_exitoso else 1)
