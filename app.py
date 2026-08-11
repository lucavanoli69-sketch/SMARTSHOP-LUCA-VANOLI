"""
SmartShop AI
Asistente inteligente de recomendaciones de productos

Aplicación Streamlit que utiliza la API de Google Gemini (SDK google-genai)
para analizar las necesidades, preferencias y presupuesto de un usuario y
generar una recomendación orientativa sobre qué características y tipo de
producto debería buscar.
"""

import streamlit as st
from google import genai
from google.genai import errors as genai_errors


# ==================================================
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# ==================================================

st.set_page_config(
    page_title="SmartShop AI",
    page_icon="🤖",
    layout="centered",
)


# ==================================================
# ESTILOS (CSS PERSONALIZADO)
# ==================================================

CUSTOM_CSS = """
<style>
    /* Fondo general */
    .stApp {
        background-color: #F4F8FC;
    }

    /* Contenedor principal más angosto y prolijo */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }

    /* Encabezado */
    .ss-header {
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
    }

    .ss-header h1 {
        color: #0B3D91;
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
    }

    .ss-header p.subtitle {
        color: #1E5AA8;
        font-size: 1.15rem;
        font-weight: 500;
        margin-top: 0;
    }

    .ss-header p.description {
        color: #33475B;
        font-size: 0.98rem;
        max-width: 650px;
        margin: 0.6rem auto 0 auto;
        line-height: 1.5;
    }

    /* Tarjetas genéricas */
    .ss-card {
        background-color: #FFFFFF;
        border: 1px solid #DCE7F5;
        border-radius: 16px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(11, 61, 145, 0.06);
    }

    .ss-card h3 {
        color: #0B3D91;
        margin-top: 0;
    }

    /* Sección "cómo funciona" */
    .ss-step {
        display: flex;
        align-items: flex-start;
        gap: 0.7rem;
        margin-bottom: 0.6rem;
    }

    .ss-step-number {
        background-color: #0B3D91;
        color: white;
        font-weight: 700;
        font-size: 0.85rem;
        min-width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .ss-step-text {
        color: #33475B;
        font-size: 0.95rem;
        padding-top: 2px;
    }

    /* Caja de resultado */
    .ss-result {
        background-color: #FFFFFF;
        border: 1px solid #CFE0F5;
        border-left: 6px solid #0B3D91;
        border-radius: 12px;
        padding: 1.6rem 1.8rem;
        margin-top: 1rem;
    }

    .ss-result {
        color: #222222 !important;
    }

    .ss-result p,
    .ss-result li,
    .ss-result span,
    .ss-result div {
        color: #222222 !important;
    }

    .ss-result h1,
    .ss-result h2,
    .ss-result h3,
    .ss-result h4 {
        color: #111111 !important;
    }

    .ss-result strong {
        color: #111111 !important;
    }

    /* Refuerzo: Streamlit envuelve el markdown generado en .stMarkdown,
       por lo que apuntamos también a esos selectores dentro de .ss-result
       para asegurar el contraste sin afectar otros textos de la app */
    .ss-result .stMarkdown p,
    .ss-result .stMarkdown li,
    .ss-result .stMarkdown span,
    .ss-result .stMarkdown div {
        color: #222222 !important;
    }

    .ss-result .stMarkdown h1,
    .ss-result .stMarkdown h2,
    .ss-result .stMarkdown h3,
    .ss-result .stMarkdown h4 {
        color: #111111 !important;
    }

    .ss-result .stMarkdown strong {
        color: #111111 !important;
    }

    /* Caja de advertencia */
    .ss-warning {
        background-color: #FFF8E6;
        border: 1px solid #F0DFA6;
        border-left: 6px solid #E0A800;
        border-radius: 12px;
        padding: 1rem 1.3rem;
        color: #6B5300;
        font-size: 0.92rem;
        margin-top: 2rem;
    }

    /* Botón principal */
    div.stButton > button {
        background-color: #0B3D91;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.6rem 1.4rem;
        border: none;
        width: 100%;
        font-size: 1.05rem;
    }

    div.stButton > button:hover {
        background-color: #0A2F70;
        color: white;
    }

    /* Footer */
    .ss-footer {
        text-align: center;
        color: #7E8FA6;
        font-size: 0.8rem;
        margin-top: 2.5rem;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==================================================
# ENCABEZADO
# ==================================================

st.markdown(
    """
    <div class="ss-header">
        <h1>🤖 SmartShop AI</h1>
        <p class="subtitle">Asistente inteligente de recomendaciones de productos</p>
        <p class="description">
            SmartShop AI utiliza Inteligencia Artificial para analizar tus necesidades,
            tu presupuesto y tus preferencias, y ayudarte a identificar qué características
            deberías buscar antes de elegir un producto.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# CLIENTE DE GEMINI
# ==================================================

def obtener_cliente_gemini():
    """
    Crea y devuelve un cliente de Gemini utilizando la API key
    almacenada de forma segura en st.secrets.
    Nunca se expone la clave en el código ni en la interfaz.
    """
    api_key = st.secrets.get("GEMINI_API_KEY", None)

    if not api_key or api_key == "PEGAR_API_KEY_AQUI":
        return None

    return genai.Client(api_key=api_key)


# Modelo Gemini utilizado para la generación de texto
MODELO_GEMINI = "gemini-3.5-flash"


# ==================================================
# CONSTRUCCIÓN DEL PROMPT
# ==================================================

def construir_prompt(categoria: str, necesidad: str, presupuesto: str, preferencias: str) -> str:
    """
    Construye el prompt que se enviará a Gemini para que actúe como
    un asesor de compras experto, siguiendo el formato de respuesta
    solicitado por la consigna académica.
    """

    prompt = f"""
Rol de la IA:
Actuás como un asesor de compras experto e imparcial, especializado en ayudar
a las personas a identificar qué características y tipo de producto deberían
buscar según sus necesidades, sin recomendar marcas, tiendas ni productos
concretos como si fueran datos verificados en tiempo real.

Objetivo:
Analizar la información proporcionada por el usuario y generar una
recomendación orientativa sobre qué especificaciones y características
debería priorizar al momento de buscar el producto, explicando el motivo
de cada recomendación.

Contexto:
El usuario está evaluando la compra de un producto y necesita orientación
para tomar una mejor decisión, ya que no siempre sabe qué características
técnicas son relevantes para su caso de uso específico.

Datos proporcionados por el usuario:
- Categoría del producto: {categoria}
- Necesidad / uso previsto: {necesidad}
- Presupuesto aproximado: {presupuesto}
- Preferencias o características importantes: {preferencias if preferencias else "No especificadas"}

Instrucciones de análisis:
1. Analizá la necesidad real del usuario y para qué va a usar el producto.
2. Tené en cuenta el presupuesto informado como un límite orientativo.
3. Considerá las preferencias indicadas por el usuario.
4. Identificá qué características técnicas o funcionales son más relevantes
   para ese caso de uso.
5. Recomendá especificaciones apropiadas (por ejemplo, tipo de componente,
   capacidad, material, funciones, etc. según corresponda a la categoría).
6. Explicá brevemente por qué cada característica recomendada es relevante.
7. Indicá qué aspectos debería verificar el usuario antes de comprar.

Limitaciones estrictas (muy importante):
- NO inventes precios actuales ni valores exactos de mercado.
- NO inventes disponibilidad de stock.
- NO inventes enlaces de tiendas ni de productos.
- NO afirmes que un producto específico está disponible si no se te
  proporcionó esa información.
- NO inventes productos concretos (marcas o modelos) como si fueran datos
  reales y verificados. Podés mencionar categorías o tipos de forma general.
- Si falta información importante para dar una mejor recomendación,
  aclaralo brevemente y sugerí qué dato adicional sería útil.
- La recomendación debe presentarse siempre como orientativa, no como una
  verdad absoluta.

Formato esperado de la respuesta (usá exactamente estos encabezados):

💡 Recomendación
(Resumen general de la recomendación en 2-4 líneas)

🎯 Características prioritarias
(Lista de las características más importantes a tener en cuenta)

📋 Especificaciones recomendadas
(Detalle de especificaciones técnicas o funcionales sugeridas, en relación al presupuesto)

❓ ¿Por qué?
(Explicación breve de por qué esas características son las más adecuadas para este caso)

⚠️ Aspectos a verificar antes de comprar
(Lista de puntos que el usuario debería chequear antes de decidir la compra)

Respondé en español, de forma clara, organizada y profesional, usando los
encabezados indicados arriba tal como están escritos.
"""
    return prompt.strip()


# ==================================================
# LLAMADA A LA API DE GEMINI
# ==================================================

def generar_recomendacion(cliente, prompt: str) -> str:
    """
    Envía el prompt a Gemini y devuelve el texto de la respuesta.
    Lanza una excepción si ocurre un error de comunicación con la API.
    """
    respuesta = cliente.models.generate_content(
        model=MODELO_GEMINI,
        contents=prompt,
    )
    return respuesta.text


# ==================================================
# FORMULARIO
# ==================================================

st.markdown('<div class="ss-card">', unsafe_allow_html=True)
st.markdown("### 📝 Contanos qué estás buscando")

with st.form(key="formulario_smartshop"):
    categoria = st.text_input(
        "Categoría del producto",
        placeholder="Ej: Notebook, Auriculares, Heladera, Bicicleta...",
    )

    necesidad = st.text_area(
        "¿Para qué necesitás el producto?",
        placeholder="Ej: La necesito para estudiar programación y usar VS Code.",
        height=90,
    )

    presupuesto = st.text_input(
        "Presupuesto aproximado",
        placeholder="Ej: USD 1000",
    )

    preferencias = st.text_area(
        "Características o preferencias importantes (opcional)",
        placeholder="Ej: 16 GB de RAM, SSD y buena batería.",
        height=90,
    )

    enviado = st.form_submit_button("🔍 Generar recomendación")

st.markdown("</div>", unsafe_allow_html=True)


# ==================================================
# LÓGICA AL ENVIAR EL FORMULARIO
# ==================================================

if enviado:
    # Validaciones de campos obligatorios
    errores = []

    if not categoria or not categoria.strip():
        errores.append("Ingresá la **categoría** del producto.")

    if not necesidad or not necesidad.strip():
        errores.append("Contanos **para qué necesitás** el producto.")

    if not presupuesto or not presupuesto.strip():
        errores.append("Ingresá un **presupuesto** aproximado.")

    if errores:
        for error in errores:
            st.warning(error)
    else:
        cliente = obtener_cliente_gemini()

        if cliente is None:
            st.error(
                "⚠️ No se encontró una API key válida de Gemini. "
                "Configurá `GEMINI_API_KEY` en `.streamlit/secrets.toml` "
                "para poder generar recomendaciones."
            )
        else:
            prompt = construir_prompt(
                categoria=categoria.strip(),
                necesidad=necesidad.strip(),
                presupuesto=presupuesto.strip(),
                preferencias=preferencias.strip() if preferencias else "",
            )

            with st.spinner("🤖 SmartShop AI está analizando tu consulta..."):
                try:
                    texto_respuesta = generar_recomendacion(cliente, prompt)

                    st.markdown(
                        f'<div class="ss-result">\n\n{texto_respuesta}\n\n</div>',
                        unsafe_allow_html=True,
                    )

                except genai_errors.APIError as e:
                    st.error(f"❌ Error de Gemini: {e}")
                except Exception as e:
                    st.error(f"❌ Error inesperado: {e}")


# ==================================================
# SECCIÓN: ¿CÓMO FUNCIONA SMARTSHOP AI?
# ==================================================

st.markdown('<div class="ss-card">', unsafe_allow_html=True)
st.markdown("### ⚙️ ¿Cómo funciona SmartShop AI?")

pasos = [
    "El usuario describe lo que necesita.",
    "Indica presupuesto y preferencias.",
    "La información se envía a un prompt diseñado específicamente.",
    "Gemini analiza la consulta.",
    "SmartShop AI muestra una recomendación personalizada.",
]

for i, paso in enumerate(pasos, start=1):
    st.markdown(
        f"""
        <div class="ss-step">
            <div class="ss-step-number">{i}</div>
            <div class="ss-step-text">{paso}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)


# ==================================================
# SECCIÓN DE LIMITACIONES
# ==================================================

st.markdown(
    """
    <div class="ss-warning">
        ⚠️ La recomendación es orientativa. Verificá siempre las especificaciones,
        disponibilidad y precios antes de realizar una compra.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="ss-footer">
        SmartShop AI · Proyecto académico · Impulsado por Google Gemini
    </div>
    """,
    unsafe_allow_html=True,
)