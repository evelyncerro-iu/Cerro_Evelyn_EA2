"""Modulo encargado de la extraccion de datos mediante tecnicas de raspado web."""

from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup


class ExtractorDiosaBq:
    """Clase especializada en extraer informacion de productos de la tienda Diosa Bq."""

    def __init__(self, agente_usuario: Optional[str] = None) -> None:
        """Inicializa el extractor con cabeceras de navegacion seguras."""
        self.encabezados_solicitud: Dict[str, str] = {
            "User-Agent": (
                agente_usuario
                if agente_usuario is not None
                else (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )
        }

    def extraer_desde_html(
        self,
        contenido_html: str,
        limite_productos: int = 10
    ) -> List[Dict[str, Any]]:
        """Analiza codigo HTML y extrae una lista estructurada de productos.

        Parametros:
            contenido_html: Texto que contiene el marcado HTML a analizar.
            limite_productos: Cantidad maxima de productos a extraer.

        Retorna:
            Lista de diccionarios con el titulo y precio crudo de cada producto.
        """
        analizador_sopa = BeautifulSoup(contenido_html, "html.parser")
        tarjetas_producto = analizador_sopa.find_all(
            "div", class_="card__content"
        )

        lista_productos_extraidos: List[Dict[str, Any]] = []
        contador_registros: int = 0

        for tarjeta_actual in tarjetas_producto:
            if contador_registros >= limite_productos:
                break

            elemento_titulo = tarjeta_actual.find(class_="card__heading")
            elemento_precio = tarjeta_actual.find(class_="price-item")

            if elemento_titulo is not None and elemento_precio is not None:
                texto_titulo = elemento_titulo.get_text(strip=True)
                texto_precio = elemento_precio.get_text(strip=True)

                if texto_titulo and texto_precio:
                    lista_productos_extraidos.append(
                        {
                            "titulo_crudo": texto_titulo,
                            "precio_crudo": texto_precio,
                            "estado_extraccion": "exitoso"
                        }
                    )
                    contador_registros += 1

        return lista_productos_extraidos

    def obtener_catalogo_remoto(
        self,
        direccion_url: str,
        limite_productos: int = 10,
        tiempo_espera_segundos: int = 15
    ) -> List[Dict[str, Any]]:
        """Realiza la peticion HTTP a la tienda en linea y extrae los productos.

        Parametros:
            direccion_url: Direccion web de la tienda mayorista.
            limite_productos: Limite de registros a recuperar.
            tiempo_espera_segundos: Tiempo maximo de espera de la peticion.

        Retorna:
            Lista estructurada de productos extraidos.
        """
        try:
            respuesta_servidor = requests.get(
                direccion_url,
                headers=self.encabezados_solicitud,
                timeout=tiempo_espera_segundos
            )
            respuesta_servidor.raise_for_status()
            return self.extraer_desde_html(
                respuesta_servidor.text,
                limite_productos=limite_productos
            )
        except requests.RequestException as error_solicitud:
            print(f"Error al conectar con la tienda en linea: {error_solicitud}")
            return []
