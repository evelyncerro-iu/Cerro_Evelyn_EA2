"""Modulo generador de reportes y visualizacion web para el despliegue continuo."""

import datetime
from typing import Any, Dict, List


class PublicadorReporteHtml:
    """Genera un sitio web estatico y accesible para publicar el catalogo procesado."""

    @staticmethod
    def generar_pagina_dashboard(
        lista_productos: List[Dict[str, Any]],
        ruta_archivo_html: str,
        ambiente_despliegue: str = "GitHub Pages (DevOps)"
    ) -> bool:
        """Construye un archivo HTML visualmente interactivo con estadisticas del catalogo."""
        total_productos: int = len(lista_productos)
        precios_validos = [
            producto.get("precio_numerico")
            for producto in lista_productos
            if producto.get("precio_numerico") is not None
        ]

        precio_promedio = (
            sum(precios_validos) / len(precios_validos)
            if precios_validos
            else 0.0
        )
        precio_maximo = max(precios_validos) if precios_validos else 0.0
        precio_minimo = min(precios_validos) if precios_validos else 0.0

        marca_temporal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        filas_tabla_html: List[str] = []
        for indice_registro, producto_item in enumerate(lista_productos, start=1):
            nombre = producto_item.get("nombre_producto", "Sin nombre")
            precio_texto = producto_item.get("precio_texto", "N/A")
            moneda = producto_item.get("moneda", "COP")
            filas_tabla_html.append(
                f"""
                <tr>
                    <td class="numero-fila">{indice_registro}</td>
                    <td class="columna-producto">{nombre}</td>
                    <td class="columna-precio">{precio_texto}</td>
                    <td><span class="etiqueta-moneda">{moneda}</span></td>
                    <td><span class="insignia-disponible">Disponible</span></td>
                </tr>
                """
            )

        cuerpo_filas = "".join(filas_tabla_html)

        plantilla_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evidencia de Aprendizaje 2 | DevOps & CI/CD</title>
    <style>
        :root {{
            --color-primario: #1e3a8a;
            --color-secundario: #0284c7;
            --color-fondo: #f8fafc;
            --color-tarjeta: #ffffff;
            --color-texto: #0f172a;
            --color-texto-suave: #64748b;
            --color-borde: #e2e8f0;
            --color-exito: #16a34a;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, sans-serif;
        }}
        body {{
            background-color: var(--color-fondo);
            color: var(--color-texto);
            padding: 2rem 1rem;
            line-height: 1.5;
        }}
        .contenedor-principal {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        header {{
            background: linear-gradient(135deg, var(--color-primario), var(--color-secundario));
            color: white;
            padding: 2.5rem 2rem;
            border-radius: 1rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }}
        header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        header p {{
            opacity: 0.9;
            font-size: 1.05rem;
        }}
        .insignias-contenedor {{
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-top: 1.25rem;
        }}
        .insignia {{
            background-color: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(4px);
            padding: 0.4rem 0.9rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        .tarjetas-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2rem;
        }}
        .tarjeta-metrica {{
            background-color: var(--color-tarjeta);
            padding: 1.5rem;
            border-radius: 0.75rem;
            border: 1px solid var(--color-borde);
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .tarjeta-metrica .titulo {{
            font-size: 0.85rem;
            color: var(--color-texto-suave);
            text-transform: uppercase;
            font-weight: 600;
        }}
        .tarjeta-metrica .valor {{
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--color-primario);
            margin-top: 0.25rem;
        }}
        .seccion-tabla {{
            background-color: var(--color-tarjeta);
            border-radius: 0.75rem;
            border: 1px solid var(--color-borde);
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            padding: 1.75rem;
            overflow-x: auto;
        }}
        .seccion-tabla h2 {{
            font-size: 1.35rem;
            margin-bottom: 1rem;
            color: var(--color-primario);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}
        th, td {{
            padding: 0.9rem 1rem;
            border-bottom: 1px solid var(--color-borde);
        }}
        th {{
            background-color: #f1f5f9;
            color: var(--color-texto-suave);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .numero-fila {{
            color: var(--color-texto-suave);
            font-weight: 600;
            width: 50px;
        }}
        .columna-producto {{
            font-weight: 500;
        }}
        .columna-precio {{
            font-weight: 700;
            color: var(--color-primario);
        }}
        .etiqueta-moneda {{
            background-color: #e0f2fe;
            color: #0369a1;
            padding: 0.2rem 0.6rem;
            border-radius: 0.35rem;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .insignia-disponible {{
            background-color: #dcfce7;
            color: var(--color-exito);
            padding: 0.25rem 0.65rem;
            border-radius: 0.35rem;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        footer {{
            text-align: center;
            margin-top: 3rem;
            color: var(--color-texto-suave);
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="contenedor-principal">
        <header>
            <h1>Flujo de Trabajo DevOps: Web Scraping & Despliegue Continuo</h1>
            <p>Evidencia de Aprendizaje 2 | Continuidad de EA1 (Diosa Bq)</p>
            <div class="insignias-contenedor">
                <span class="insignia">Entorno: {ambiente_despliegue}</span>
                <span class="insignia">Pipeline: GitHub Actions CI/CD</span>
                <span class="insignia">Estado: Despliegue Exitoso</span>
                <span class="insignia">Generado: {marca_temporal}</span>
            </div>
        </header>

        <section class="tarjetas-grid">
            <div class="tarjeta-metrica">
                <div class="titulo">Productos Procesados</div>
                <div class="valor">{total_productos}</div>
            </div>
            <div class="tarjeta-metrica">
                <div class="titulo">Precio Promedio</div>
                <div class="valor">${precio_promedio:,.0f} COP</div>
            </div>
            <div class="tarjeta-metrica">
                <div class="titulo">Precio Minimo</div>
                <div class="valor">${precio_minimo:,.0f} COP</div>
            </div>
            <div class="tarjeta-metrica">
                <div class="titulo">Precio Maximo</div>
                <div class="valor">${precio_maximo:,.0f} COP</div>
            </div>
        </section>

        <section class="seccion-tabla">
            <h2>Catalogo de Productos Extraidos</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Descripcion del Producto</th>
                        <th>Precio Unitario</th>
                        <th>Divisa</th>
                        <th>Disponibilidad</th>
                    </tr>
                </thead>
                <tbody>
                    {cuerpo_filas}
                </tbody>
            </table>
        </section>

        <footer>
            <p>Evelyn Cerro &bull; Control de Versiones Git &bull; CI/CD GitHub Actions</p>
        </footer>
    </div>
</body>
</html>
"""
        try:
            with open(ruta_archivo_html, mode="w", encoding="utf-8") as archivo_salida:
                archivo_salida.write(plantilla_html)
            return True
        except (IOError, OSError) as error_escritura:
            print(f"Error al escribir el archivo de reporte HTML: {error_escritura}")
            return False
