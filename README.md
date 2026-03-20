# 🥗 SmartFridge: Vision-Based Recipe Recommender System
### *Sistema de Visión y Recomendación de Recetas Inteligente*

Este proyecto combina **Computer Vision**, **Procesamiento de Lenguaje Natural (NLP)** y **Sistemas de Recomendación** para automatizar la gestión de alimentos en un frigorífico y reducir el desperdicio de comida.

---

## Descripción del Proyecto
**SmartFridge** transforma una fotografía de la nevera en un inventario digital dinámico. A diferencia de los sistemas genéricos, este proyecto utiliza un enfoque de tres capas (Localización + OCR + LLM) para identificar con precisión marcas y productos específicos, cruzando estos datos con un motor de recomendaciones para sugerir qué cocinar.

[![Watch the video]
(https://www.youtube.com/watch?v=up4Wf_Aq_P0)

---

## 🛠️ Arquitectura Técnica / Technical Stack

| Componente | Tecnología | Función |
| :--- | :--- | :--- |
| **Object Detection** | Google Vision API | Localizar alimentos (Bounding Boxes). |
| **Brand Recognition** | OCR (Google Vision) | Leer etiquetas y nombres específicos de productos. |
| **Text Normalization** | LLM (OpenAI/Gemini) | Mapear texto de etiquetas a ingredientes base (limpieza). |
| **Database** | SQLite | Almacenar inventario, fechas de entrada y estado. |
| **Recommendation** | TBD API | Motor de búsqueda de recetas basado en ingredientes. |
| **Environment** | Google Colab | Entorno de desarrollo colaborativo. |

---

## 🚀 Instalación y Uso / Setup & Usage

### 1. Requisitos / Prerequisites
* Cuenta de **Google Cloud** con la Vision API habilitada.
* API Key de **TBD**.
* Cuenta de **Kaggle** (para descargar datasets).

### 2. Configuración / Configuration
Sube tus archivos de credenciales a la raíz de tu entorno en Colab:
* `google_vision_key.json`
* `kaggle.json`

### 3. Ejecución / Execution
Abre el notebook `SmartFridge_Main.ipynb` y ejecuta las celdas en orden para:
1. Clonar el repositorio.
2. Procesar la imagen mediante la API de Google.
3. Normalizar ingredientes con el LLM.
4. Obtener sugerencias de recetas personalizadas.

---

## 📊 Esquema de Datos / Database Schema

El sistema mantiene la persistencia mediante una base de datos SQLite con la siguiente relación:



* **Inventario:** Almacena el `id`, `nombre_ocr`, `ingrediente_limpio` y `fecha_captura`.
* **Usuarios:** Almacena preferencias dietéticas y alergias para filtrar las recetas.

---

## 📅 Roadmap & Future Work / Trabajo Futuro

* [ ] **Deployment:** Crear una interfaz web con **Streamlit** o **Flask**.
* [ ] **Mobile App:** Integración con **Flutter** para capturar fotos desde el móvil.
* [ ] **Expiration Tracking:** Alertas automáticas de caducidad mediante OCR de fechas.
* [ ] **Edge AI:** Migrar el modelo a **AutoML Edge (TFLite)** para funcionamiento offline.

---
## Economics del Proyecto

Se está ejecutando el proyecto en un entorno **DEMO**, sin coste. Para productivizar la demo, es necesario moverse a **Google Cloud Vertex AI**. La estructura de costes se basa en el volumen de información (tokens) enviada al modelo `gemini-1.5-flash`.

### 1. Estructura de Precios (Pago por uso)
Google factura por cada 1.000 tokens (aproximadamente 750 palabras). En el caso de Flash, el precio cambia según la longitud del contexto:

| Tipo de Dato | Precio (<128k tokens) | Precio (>128k tokens) |
| :--- | :--- | :--- |
| **Input (Entrada)** | $0.075 / 1M tokens | $0.15 / 1M tokens |
| **Output (Salida)** | $0.30 / 1M tokens | $0.60 / 1M tokens |
| **Imágenes** | $0.00002 / imagen | $0.00004 / imagen |

---

### 2. Estimación de costes para "Nevera Inteligente"
Cálculo estimado para una aplicación profesional estándar:

* **Petición de imagen:** 258 tokens fijos.
* **Prompt de texto:** ~200 tokens.
* **Respuesta (JSON):** ~300 tokens.

**Coste por análisis:**
* **Input:** 458 tokens $\approx$ $0.000034
* **Output:** 300 tokens $\approx$ $0.00009
* **Total:** **< $0.00015 por análisis.**

---

### 3. Progresión de costes por escala
A continuación se muestra la proyección de costes según el volumen de uso:

| Volumen de Análisis | Coste Estimado (USD) |
| :--- | :--- |
| 1 análisis | 0,00015 $ |
| 10 análisis | 0,0015 $ |
| 100 análisis | 0,015 $ |
| 1.000 análisis | 0,15 $ |
| 10.000 análisis | 1,5 $ |
| 100.000 análisis | 15 $ |
| 1.000.000 análisis | 150 $ |



---

## Herramientas del proyecto

Se usan como herramientas de desarrollo:
- higgub - como repositorio
- visual studio y colab - como herramientas de desarrollo
- python y herramientas de google - librerías de desarrollo


---
## 👥 Colaboradores / Contributors
* **Isabel Castrejon, David RH, Julio Cesar, JositoRené** - Data Engineering & API Integration
