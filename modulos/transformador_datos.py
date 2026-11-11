"""Modulo dedicado a la limpieza, normalizacion y exportacion de datos procesados."""

import csv
import json
import re
from typing import Any, Dict, List, Optional


class TransformadorProductos:
    """Clase para procesar, limpiar y transformar los registros de productos extraidos."""

    @staticmethod
    def limpiar_texto(texto_original: str) -> str:
        """Elimina espacios redundantes y caracteres de control."""
        if not texto_original:
            return ""
        palabras_separadas = texto_original.split()
        return " ".join(palabras_separadas).strip()

    @staticmethod
    def limpiar_precio_numerico(precio_texto: str) -> Optional[float]:
        """Extrae el valor numerico del precio en formato decimal.

        Ejemplo:
            '$17,000 COP' -> 17000.0
        """
        if not precio_texto:
            return None

        coincidencia_numerica = re.search(r"(\d[\d.,]*)", precio_texto)
        if not coincidencia_numerica:
            return None

        cadena_numerica = coincidencia_numerica.group(1)
        # En Colombia y formato local, las comas o puntos separan miles
        cadena_sin_separador_miles = cadena_numerica.replace(",", "").replace(".", "")

        try:
            return float(cadena_sin_separador_miles)
        except ValueError:
            return None

    def estructurar_producto(self, registro_crudo: Dict[str, Any]) -> Dict[str, Any]:
        """Transforma un registro crudo en un diccionario con campos estandarizados."""
        titulo_limpio = self.limpiar_texto(registro_crudo.get("titulo_crudo", ""))
        texto_precio = self.limpiar_texto(registro_crudo.get("precio_crudo", ""))
        valor_numerico = self.limpiar_precio_numerico(texto_precio)

        moneda_detectada = "COP" if "COP" in texto_precio.upper() else "USD"

        return {
            "nombre_producto": titulo_limpio,
            "precio_texto": texto_precio,
            "precio_numerico": valor_numerico,
            "moneda": moneda_detectada,
            "disponible": valor_numerico is not None and valor_numerico > 0
        }

    def procesar_catalogo(
        self,
        lista_cruda: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Aplica la transformacion y limpieza a toda la coleccion de productos."""
        catalogo_transformado: List[Dict[str, Any]] = []

        for elemento_actual in lista_cruda:
            producto_normalizado = self.estructurar_producto(elemento_actual)
            catalogo_transformado.append(producto_normalizado)

        return catalogo_transformado

    @staticmethod
    def exportar_a_json(
        datos_catalogo: List[Dict[str, Any]],
        ruta_archivo_destino: str
    ) -> bool:
        """Serializa el catalogo a formato JSON con codificacion UTF-8."""
        try:
            with open(ruta_archivo_destino, mode="w", encoding="utf-8") as descriptor_archivo:
                json.dump(
                    datos_catalogo,
                    descriptor_archivo,
                    ensure_ascii=False,
                    indent=2
                )
            return True
        except (IOError, OSError) as error_guardado:
            print(f"Error al exportar datos a formato JSON: {error_guardado}")
            return False

    @staticmethod
    def exportar_a_csv(
        datos_catalogo: List[Dict[str, Any]],
        ruta_archivo_destino: str
    ) -> bool:
        """Exporta los productos a un archivo plano delimitado por comas."""
        if not datos_catalogo:
            return False

        nombres_columnas = list(datos_catalogo[0].keys())

        try:
            with open(ruta_archivo_destino, mode="w", encoding="utf-8", newline="") as archivo_csv:
                escritor_csv = csv.DictWriter(
                    archivo_csv,
                    fieldnames=nombres_columnas
                )
                escritor_csv.writeheader()
                escritor_csv.writerows(datos_catalogo)
            return True
        except (IOError, OSError) as error_guardado:
            print(f"Error al exportar datos a formato CSV: {error_guardado}")
            return False
