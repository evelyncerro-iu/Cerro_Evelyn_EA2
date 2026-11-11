# Documentación Técnica del Flujo de Trabajo DevOps y Control de Versiones

## Evidencia de Aprendizaje 2 (EA2)
**Proyecto:** Sistema de Extracción Automatizada, Pruebas y Despliegue Continuo de Datos de Comercio Electrónico (Diosa Bq)  
**Continuidad:** Basado en la Evidencia de Aprendizaje 1 (`cuadernos/Cerro_Evelyn_Analizando_EA1.ipynb`)  
**Autor:** Evelyn Cerro  
**Institución:** Institución Universitaria Digital de Antioquia (IU Digital)  

---

## 1. Formulación de Objetivos del Proyecto

### 1.1 Objetivo General
Desarrollar e implementar un flujo de trabajo DevOps integral para el proyecto de software de extracción y análisis de comercio electrónico, utilizando Git y GitHub como plataforma de control de versiones y colaboración, e implementando un pipeline automatizado de Integración Continua (CI) y Despliegue Continuo (CD) con GitHub Actions que garantice la calidad del código mediante pruebas automatizadas y ejecute el despliegue continuo en un entorno web en la nube accesible, estable y de alta disponibilidad.

### 1.2 Objetivos Específicos
1. **Modularizar y Refactorizar:** Transformar el código experimental de web scraping de la Evidencia 1 (BeautifulSoup, Selenium y Scrapy sobre Diosa Bq) en una arquitectura de software desacoplada, orientada a objetos, modular y con tipado estricto.
2. **Estrategia de Control de Versiones (Git & GitHub):** Implementar una estrategia de ramificación estructurada (*GitFlow*) con ramas principales (`main`, `desarrollo`), ramas de soporte de características (*feature branches*), commits semánticos en español y simulación de fusiones vía *Pull Requests* con revisión de código.
3. **Automatización de Pruebas e Integración Continua (CI):** Diseñar y configurar un flujo de trabajo automatizado en GitHub Actions que valide estándares de calidad mediante análisis estático de código (*Flake8*) y ejecute suites completas de pruebas unitarias (*Pytest*) ante cada cambio o solicitud de integración.
4. **Despliegue Continuo (CD) y Disponibilidad:** Implementar un pipeline de despliegue automático hacia un entorno en la nube accesible (*GitHub Pages*), complementado con contenedorización en *Docker* para garantizar portabilidad y reproducibilidad en cualquier servidor.
5. **Documentación Integral y Trazabilidad:** Proporcionar una bitácora técnica exhaustiva y transparente que describa la arquitectura, los comandos ejecutados, la matriz de pruebas y el ciclo de vida del software.

---

## 2. Continuidad con la Evidencia de Aprendizaje 1 (EA1)

En la **Evidencia de Aprendizaje 1**, se realizó un análisis exploratorio y experimental de extracción de datos sobre la plataforma de comercio electrónico mayorista **Diosa Bq** (`https://www.diosabq.com/`) utilizando tres tecnologías en un cuaderno Jupyter:
* **BeautifulSoup:** Extracción estática mediante análisis del árbol DOM y selectores CSS (`.card__content`, `.card__heading`, `.price-item`).
* **Selenium WebDriver:** Extracción dinámica con renderizado de navegador Chromium en modo sin cabeza (*headless*).
* **Scrapy:** Motor asíncrono con reactor de red Twisted para rastreo concurrente.

En esta **Evidencia de Aprendizaje 2**, se toma dicho producto y se traslada al estándar de la ingeniería de software profesional y la cultura DevOps:
* Se preserva el archivo original en la ruta `cuadernos/Cerro_Evelyn_Analizando_EA1.ipynb`.
* Se extrae la lógica a módulos independientes (`modulos/extractor_datos.py`, `modulos/transformador_datos.py`, `modulos/publicador_reporte.py`).
* Se añade una capa de pruebas automatizadas con datos reales y datos simulados (*fixtures*).
* Se crea un pipeline que extrae, transforma a JSON/CSV y genera un sitio web responsivo listo para producción.

---

## 3. Estrategia de Ramificación y Gestión de Versiones (GitFlow)

El control de versiones se organizó bajo una estrategia estructurada que previene la inserción de errores en el código productivo:

```
[main] -----------------------------------------------------> [v1.0.0 Despliegue Producción]
   ^                                                                 ^
   | (Merge Release / Pull Request)                                  | (Merge CD)
   |                                                                 |
[desarrollo] -----------------------------------> [Integración CI] --+
   ^                                 ^
   |                                 |
   +-- [caracteristica/modularizacion]
   |
   +-- [caracteristica/pruebas-unitarias]
   |
   +-- [caracteristica/automatizacion-ci-cd]
```

### 3.1 Estructura de Ramas
* **`main`:** Rama de producción. Contiene exclusivamente código verificado, probado y listo para ser desplegado. Los commits en esta rama disparan automáticamente el despliegue continuo hacia el entorno en la nube.
* **`desarrollo`:** Rama de integración continua. Agrupa las funcionalidades desarrolladas y ejecuta las validaciones de calidad antes de su paso a producción.
* **`caracteristica/*` (*Feature branches*):** Ramas temporales creadas para desarrollar componentes específicos (ej. modularización del scraper, pruebas unitarias, configuración de pipelines).

### 3.2 Convención de Commits Semánticos
Cada confirmación de cambios sigue la convención semántica en español:
* `feat:` Incorporación de una nueva funcionalidad o módulo.
* `test:` Adición o refactorización de pruebas unitarias.
* `ci:` Configuración de pipelines y automatización en GitHub Actions.
* `docs:` Creación y actualización de documentación y guías.
* `refactor:` Optimización del código sin alterar su comportamiento funcional.
* `chore:` Tareas rutinarias de configuración y estructura de carpetas.

---

## 4. Pipeline de CI/CD con GitHub Actions

La automatización se gestiona mediante dos flujos de trabajo (*workflows*) independientes en `.github/workflows/`:

### 4.1 Integración Continua (`integracion_continua.yml`)
* **Disparadores (*Triggers*):** Eventos `push` y `pull_request` dirigidos a las ramas `main` y `desarrollo`.
* **Matriz de Entornos:** Valida compatibilidad en Python 3.11 y Python 3.12 sobre máquinas virtuales `ubuntu-latest`.
* **Etapas (*Jobs*):**
  1. **Checkout del código:** Clona el repositorio con `actions/checkout@v4`.
  2. **Configuración del Runtime:** Establece la versión de Python especificada y activa la caché de dependencias `pip`.
  3. **Instalación de Dependencias:** Instala `requirements.txt` con validación de hashes.
  4. **Análisis Estático (Linter):** Ejecuta `flake8` verificando adherencia a PEP 8, longitud máxima de línea y ausencia de variables no utilizadas o mal tipadas.
  5. **Pruebas Automatizadas:** Ejecuta `pytest` sobre el directorio `pruebas/`, garantizando que todas las aserciones pasen con éxito.

### 4.2 Despliegue Continuo (`despliegue_continuo.yml`)
* **Disparadores (*Triggers*):** Evento `push` en la rama `main` tras la aprobación de la integración.
* **Permisos del Token:** `contents: write`, `pages: write`, `id-token: write`.
* **Etapas (*Jobs*):**
  1. **Pre-validación:** Ejecución rápida de la suite de pruebas unitarias.
  2. **Ejecución del Flujo:** Se ejecuta `python principal.py`, obteniendo el catálogo fresco y compilando los archivos estáticos en la carpeta `dist/` (`index.html`, `productos.json`, `productos.csv`).
  3. **Empaquetado de Artefactos:** Carga del directorio `dist/` mediante `actions/upload-pages-artifact@v3`.
  4. **Despliegue a la Nube:** Publicación oficial en **GitHub Pages** mediante `actions/deploy-pages@v4`.
  5. **Sincronización:** Publicación paralela en la rama `gh-pages` con `peaceiris/actions-gh-pages@v4`.

---

## 5. Entorno de Despliegue en la Nube y Contenedorización

El proyecto ofrece doble estrategia de despliegue para satisfacer cualquier infraestructura:

### 5.1 Despliegue en la Nube (GitHub Pages)
* **URL Pública de Acceso:** `https://evelyncerro-iu.github.io/Cerro_Evelyn_EA2/`
* **Características:**
  * Accesibilidad pública 24/7 sin costo de infraestructura.
  * Interfaz responsiva con métricas clave (Total de productos, precios mínimos, promedio y máximos en pesos colombianos COP).
  * Tabla interactiva con el estado de inventario y disponibilidad.

### 5.2 Despliegue en Contenedores (Docker & Docker Compose)
Para entornos de servidor empresarial o clústeres en la nube (AWS ECS, Google Cloud Run, Azure Container Instances):
```bash
# Construcción y arranque del contenedor
docker compose up --build -d

# Acceso local o en servidor
http://localhost:8080
```

---

## 6. Conclusiones de la Implementación DevOps

1. **Trazabilidad y Calidad Garantizada:** La adopción de Git y GitHub junto a GitFlow asegura un historial transparente y auditable, donde ningún código llega a producción sin superar las pruebas automáticas.
2. **Cultura Shift-Left:** Al ejecutar los linters y pruebas unitarias en la fase temprana de Pull Request (CI), se detectan inconsistencias y errores de formato antes de cualquier despliegue.
3. **Continuidad y Escalabilidad:** La transición de un cuaderno de laboratorio (EA1) a un paquete modular automatizado (EA2) demuestra cómo el ciclo de vida DevOps transforma prototipos en productos de software estables y listos para producción.
