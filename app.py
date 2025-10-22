# -*- coding: utf-8 -*-
import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# =========================
# CONFIG PÁGINA
# =========================
st.set_page_config(page_title="MQTT Control", page_icon="📡", layout="centered")

# =========================
# ESTILOS (tema oscuro pro + animaciones sobrias)
# =========================
st.markdown("""
<style>
:root{
  --bg:#0b1120; --bg2:#0f172a; --panel:#111827; --border:#1f2937;
  --text:#ffffff; --muted:#cbd5e1; --accent:#22d3ee; --accent2:#6366f1; --ok:#10b981; --warn:#f59e0b;
}
[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(1000px 600px at 100% 0%, rgba(99,102,241,.12), transparent 60%),
    radial-gradient(900px 600px at 0% 0%, rgba(34,211,238,.10), transparent 60%),
    linear-gradient(180deg, var(--bg) 0%, var(--bg2) 100%) !important;
  color: var(--text) !important;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial;
}
main .block-container{ padding-top: 1.6rem; padding-bottom: 2.1rem; max-width: 860px; }

h1,h2,h3{ color:#fff; letter-spacing:-.02em; }
h1 .grad{
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  -webkit-background-clip: text; background-clip:text; color:transparent;
}

/* Tarjetas */
.card{
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.1rem 1.3rem;
  box-shadow: 0 22px 60px rgba(0,0,0,.55);
  animation: fadeIn .45s ease;
}
@keyframes fadeIn{ from{opacity:0; transform: translateY(8px)} to{opacity:1; transform:none} }

/* Botones primarios */
.stButton > button{
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  border:0; color:#fff; font-weight:700;
  border-radius:999px; padding:.8rem 1.2rem;
  box-shadow:0 12px 36px rgba(99,102,241,.35);
  transition: transform .14s ease, box-shadow .14s ease, filter .14s ease;
}
.stButton > button:hover{ transform: translateY(-1px) scale(1.01); box-shadow:0 18px 52px rgba(99,102,241,.5); filter:brightness(1.06) }

/* Botones secundarios (ON/OFF) */
.btn-row > div > button{
  width:100%;
  border-radius: 14px;
  padding:.75rem 1rem; font-weight:700; border:1px solid #22314a;
  background:#0e1830; color:#e6f1ff;
}
.btn-row > div > button:hover{ border-color:#4b64ff; background:#122146 }

/* Slider track/handle */
.stSlider [data-baseweb="slider"] > div > div{ background:#1e2b49 !important; }
.stSlider [role="slider"]{ background: var(--accent) !important; }

/* Alertas compactas */
.stAlert{ background:#10203d !important; border-left:4px solid var(--accent2); border-radius:12px; }

/* Badges */
.badge{
  display:inline-block; font-size:.8rem; padding:.18rem .55rem; border-radius:999px;
  background:#0e2039; border:1px solid #224268; color:#9cdcff; margin-left:.5rem;
}

/* Logs */
.log{
  background:#0f172a; border:1px solid #22314a; border-radius:12px;
  padding:.8rem 1rem; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  color:#e5e7eb; max-height:220px; overflow:auto;
}
footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

def card_start(): st.markdown('<div class="card">', unsafe_allow_html=True)
def card_end():   st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ESTADO
# =========================
if "log" not in st.session_state: st.session_state.log = []

# =========================
# MQTT CALLBACKS (sin cambios de arquitectura)
# =========================
values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    st.session_state.log.append("✅ Dato publicado correctamente.")
    # print para logs de servidor
    print("el dato ha sido publicado")

def on_message(client, userdata, message):
    time.sleep(0.2)
    payload = str(message.payload.decode("utf-8"))
    st.session_state.log.append(f"📥 RX [{message.topic}]: {payload}")

# =========================
# CONEXIÓN (valores por defecto)
# =========================
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# =========================
# HEAD
# =========================
st.markdown("## 📡 <span class='grad'>MQTT Control</span>", unsafe_allow_html=True)
st.caption(f"Versión de Python: {platform.python_version()}  ·  Broker por defecto: **{broker}:{port}**")

# =========================
# CONTROLES
# =========================
card_start()
st.markdown("### Acciones digitales <span class='badge'>ON/OFF</span>", unsafe_allow_html=True)
c1, c2 = st.columns(2, gap="small")
with c1:
    st.markdown('<div class="btn-row">', unsafe_allow_html=True)
    if st.button("ON"):
        act1="ON"
        c = paho.Client("GIT-HUB")
        c.on_publish = on_publish
        c.connect(broker, port)
        message = json.dumps({"Act1": act1})
        c.publish("cmqtt_s", message)
        st.success("Enviado: Act1=ON")
        st.session_state.log.append("🚀 TX [cmqtt_s]: {\"Act1\":\"ON\"}")
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="btn-row">', unsafe_allow_html=True)
    if st.button("OFF"):
        act1="OFF"
        c = paho.Client("GIT-HUB")
        c.on_publish = on_publish
        c.connect(broker, port)
        message = json.dumps({"Act1": act1})
        c.publish("cmqtt_s", message)
        st.warning("Enviado: Act1=OFF")
        st.session_state.log.append("🚀 TX [cmqtt_s]: {\"Act1\":\"OFF\"}")
    st.markdown('</div>', unsafe_allow_html=True)
card_end()

card_start()
st.markdown("### Valor analógico <span class='badge'>0–100</span>", unsafe_allow_html=True)
values = st.slider('Selecciona el valor', 0.0, 100.0, 50.0)
st.write('Valor:', f"**{values:.2f}**")

if st.button('Enviar valor analógico'):
    c = paho.Client("GIT-HUB")
    c.on_publish = on_publish
    c.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    c.publish("cmqtt_a", message)
    st.info(f"Enviado: Analog={values:.2f}")
    st.session_state.log.append(f"🚀 TX [cmqtt_a]: {{\"Analog\": {values:.2f}}}")
card_end()

# =========================
# LOG DE MENSAJES (RX/TX)
# =========================
card_start()
st.markdown("### Monitor de mensajes")
if st.session_state.log:
    st.markdown("<div class='log'>" + "<br/>".join(st.session_state.log[-200:]) + "</div>", unsafe_allow_html=True)
else:
    st.info("Aún no hay mensajes en el monitor. Envía algo para ver actividad.")
card_end()

# =========================
# NOTA
# =========================
st.caption("UI dark, limpia y legible · Animaciones discretas · Arquitectura original de publicación MQTT intacta.")
