# 🤖 SmartShop AI

**Asistente inteligente de recomendaciones de productos**

## 📌 Descripción del proyecto

SmartShop AI es una aplicación web que utiliza Inteligencia Artificial
(Google Gemini) para ayudar a los usuarios a identificar qué características
y tipo de producto deberían buscar, según sus necesidades, presupuesto y
preferencias.

Este proyecto corresponde a una entrega académica y **no es un e-commerce
completo**: no incluye carrito de compras, sistema de usuarios, login, pagos,
base de datos, catálogo real ni integración con tiendas. Su objetivo es
demostrar el uso concreto de Inteligencia Artificial para resolver una
problemática puntual mediante una tarea específica: la generación de
recomendaciones personalizadas.

## 🧩 Problemática

En el comercio electrónico actual suelen presentarse los siguientes problemas:

- Búsqueda dificultosa de productos.
- Consultas repetitivas por parte de los usuarios.
- Atención al cliente limitada.
- Abandono del carrito de compras.
- Pérdida de ventas.

## 💡 Solución propuesta

Utilizar Inteligencia Artificial para brindar una atención personalizada,
analizando las necesidades de cada usuario y generando recomendaciones de
producto precisas y orientativas, sin depender de un catálogo real ni de
datos de stock o precios en tiempo real.

## 🎯 Objetivo de la aplicación

Recibir las necesidades, preferencias y presupuesto de un usuario, y utilizar
Inteligencia Artificial (Gemini) para generar una recomendación personalizada
sobre qué características y tipo de producto debería buscar.

## ⚙️ Funcionamiento

1. El usuario describe lo que necesita.
2. Indica presupuesto y preferencias.
3. La información se envía a un prompt diseñado específicamente para
   comportarse como un asesor de compras.
4. Gemini analiza la consulta.
5. SmartShop AI muestra una recomendación personalizada, organizada en
   secciones:
   - 💡 Recomendación
   - 🎯 Características prioritarias
   - 📋 Especificaciones recomendadas
   - ❓ ¿Por qué?
   - ⚠️ Aspectos a verificar antes de comprar

## 🛠️ Tecnologías utilizadas

- **Python**
- **Streamlit** — interfaz web
- **Google Gemini API** — generación de recomendaciones mediante IA
- **google-genai** — SDK oficial actual de Google para Python

## 📁 Estructura del proyecto

```
smartshop-ai/
│
├── app.py                     # Aplicación principal de Streamlit
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Este archivo
├── .gitignore                 # Archivos y carpetas excluidos del repositorio
└── .streamlit/
    └── secrets.toml           # Plantilla para la API key (sin clave real)
```

### Función de cada archivo

- **app.py**: contiene toda la lógica de la aplicación — la interfaz, el
  formulario, la construcción del prompt, la conexión con la API de Gemini
  y la presentación del resultado.
- **requirements.txt**: lista las librerías necesarias para ejecutar el
  proyecto (`streamlit` y `google-genai`).
- **.streamlit/secrets.toml**: archivo donde se debe colocar la API key
  personal de Gemini. Nunca debe subirse a un repositorio público con una
  clave real cargada.
- **.gitignore**: evita que se suban por error archivos sensibles (como
  `secrets.toml`) o carpetas innecesarias (entornos virtuales, caché de
  Python, etc.).

## 🚀 Instalación

1. Cloná o descargá el proyecto.
2. Creá un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
```

3. Instalá las dependencias:

```bash
pip install -r requirements.txt
```

## 🔑 Configuración de la API key

1. Obtené una API key de Google Gemini desde Google AI Studio.
2. Abrí el archivo `.streamlit/secrets.toml`.
3. Reemplazá el valor de ejemplo por tu clave real:

```toml
GEMINI_API_KEY = "TU_API_KEY_AQUI"
```

⚠️ **Importante:** nunca subas tu API key real a un repositorio público.
El archivo `.streamlit/secrets.toml` ya está incluido en `.gitignore` para
evitar que esto suceda por error.

Si vas a publicar la aplicación en **Streamlit Community Cloud**, la API key
debe configurarse desde el panel de "Secrets" de la propia plataforma, no
subiendo el archivo `secrets.toml` al repositorio.

## ▶️ Ejecución local

Una vez instaladas las dependencias y configurada la API key, ejecutá:

```bash
streamlit run app.py
```

Esto abrirá la aplicación automáticamente en tu navegador
(por defecto en `http://localhost:8501`).

## 🧭 Cómo utilizar la aplicación

1. Completá el formulario con:
   - Categoría del producto (ej: Notebook).
   - Para qué necesitás el producto.
   - Presupuesto aproximado.
   - Características o preferencias importantes (opcional).
2. Presioná el botón **"🔍 Generar recomendación"**.
3. SmartShop AI enviará la información a Gemini mediante un prompt diseñado
   específicamente para actuar como asesor de compras.
4. La recomendación generada se mostrará organizada en secciones claras,
   junto con los aspectos que deberías verificar antes de comprar.

## 🤝 Integración con Gemini

La aplicación utiliza el SDK oficial `google-genai` para crear un cliente de
Gemini a partir de la API key almacenada de forma segura en
`st.secrets["GEMINI_API_KEY"]`. Los datos ingresados por el usuario se
incorporan a un prompt estructurado (rol, objetivo, contexto, instrucciones
de análisis y formato de respuesta) que le indica al modelo cómo comportarse
como asesor de compras y qué limitaciones respetar, evitando que invente
precios, disponibilidad, enlaces o productos concretos como si fueran datos
reales.

## 🔒 Advertencia de seguridad

- Nunca compartas ni subas tu API key real a repositorios públicos.
- El archivo `.streamlit/secrets.toml` debe mantenerse fuera del control de
  versiones (ya está excluido mediante `.gitignore`).
- Las recomendaciones generadas por la IA son **orientativas**: siempre hay
  que verificar especificaciones, disponibilidad y precios reales antes de
  realizar una compra.

  ## 🤝 Presentacion Google slide

  https://docs.google.com/presentation/d/1a5unRD_6_nSalWDbDNEi-Sn8nyRcvgg__2k6dr7hoWI/edit?usp=sharing

---

Proyecto académico — SmartShop AI.
