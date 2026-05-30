import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from gemini_agent import (
    get_kpis, get_orders_by_month, get_revenue_by_country,
    get_revenue_by_category, get_revenue_by_brand,
    get_scatter_data, ask_agent
)

LOOKER_URL = "https://datastudio.google.com/u/1/reporting/490eb8ec-ba24-44d6-bffa-795a342f3ad1"
BLUE = "#0d47a1"

st.set_page_config(page_title="Supply Chain Analytics", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background:#f8f9fa; color:#202124; }
    .block-container { padding: 24px 32px !important; max-width: 1400px; }
    .kpi-card { background:#fff; border:1px solid #dadce0; border-radius:8px; padding:16px 20px; text-align:center; }
    .kpi-label { font-size:11px; font-weight:500; color:#5f6368; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px; }
    .kpi-value { font-family:'Google Sans',sans-serif; font-size:32px; font-weight:400; color:#202124; line-height:1; }
    .section-header { font-family:'Google Sans',sans-serif; font-size:14px; font-weight:500; color:#202124; padding-bottom:8px; border-bottom:2px solid #0d47a1; display:inline-block; }
    .link-btn { display:inline-flex; align-items:center; gap:8px; background:#0d47a1; color:#fff !important; text-decoration:none !important; padding:8px 16px; border-radius:4px; font-size:13px; font-weight:500; width:100%; justify-content:center; box-sizing:border-box; }
    .link-btn-outline { display:inline-flex; align-items:center; gap:8px; background:#fff; color:#0d47a1 !important; text-decoration:none !important; padding:8px 16px; border-radius:4px; font-size:13px; font-weight:500; width:100%; justify-content:center; box-sizing:border-box; border:1px solid #0d47a1; margin-top:8px; }
    .chat-box { background:#fff; border:1px solid #dadce0; border-radius:8px; padding:16px; max-height:380px; overflow-y:auto; margin-bottom:12px; }
    .msg-user { background:#e8f0fe; border-radius:8px 8px 2px 8px; padding:10px 14px; margin:8px 0 8px 60px; font-size:14px; }
    .msg-agent { background:#f1f3f4; border-left:3px solid #0d47a1; border-radius:0 8px 8px 0; padding:10px 14px; margin:8px 60px 8px 0; font-size:14px; }
    .msg-lbl { font-size:11px; color:#5f6368; font-weight:500; margin-bottom:2px; }
    .badge { display:inline-flex; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:500; }
    .badge-gemini { background:#e6f4ea; color:#137333; }
    .badge-claude { background:#fce8e6; color:#c5221f; }
    [data-testid="stSidebar"] { background:#fff; border-right:1px solid #dadce0; }
    .stButton button { background:#fff; border:1px solid #dadce0; border-radius:4px; color:#0d47a1; font-size:13px; font-weight:500; width:100%; text-align:left; padding:8px 12px; }
    .stButton button:hover { background:#e8f0fe; }
</style>
""", unsafe_allow_html=True)

def plotly_base(title="", height=300):
    return dict(
        paper_bgcolor="white", plot_bgcolor="white", height=height,
        font=dict(family="Roboto, sans-serif", color="#202124", size=11),
        margin=dict(l=16, r=80, t=40, b=16),
        title=dict(text=title, font=dict(size=13, color="#202124"), x=0),
        showlegend=False
    )

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <p style="font-family:'Google Sans',sans-serif;font-size:16px;font-weight:700;color:#202124;margin:0 0 2px 0">Supply Chain AI</p>
    <a href="https://github.com/rreghine" target="_blank" style="font-size:12px;color:#0d47a1;text-decoration:none;">github.com/rreghine</a>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<a href="{LOOKER_URL}" target="_blank" class="link-btn">Abrir Looker Studio</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://github.com/rreghine/supply-chain-analytics-gcp" target="_blank" class="link-btn-outline">Ver no GitHub</a>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Modelo de IA**")
    model_choice = st.radio("", ["gemini", "claude"],
        format_func=lambda x: "Gemini 2.5 Flash" if x == "gemini" else "Claude Opus 4.8",
        label_visibility="collapsed")
    bc = "badge-gemini" if model_choice == "gemini" else "badge-claude"
    bl = "Gemini 2.5 Flash" if model_choice == "gemini" else "Claude Opus 4.8"
    st.markdown(f'<span class="badge {bc}">{bl}</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Perguntas sugeridas**")
    for s in ["Qual o principal gargalo?", "Quais paises tem melhor performance?",
              "Como melhorar o on-time delivery?", "Qual categoria tem mais oportunidade?",
              "Analise o lead time da operacao"]:
        if st.button(s, key=s):
            st.session_state.suggested_question = s
    st.markdown("---")
    st.caption("BigQuery + dbt + Vertex AI + Looker Studio")

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<p style="font-family:'Google Sans',sans-serif;font-size:22px;font-weight:700;color:#202124;margin:0">Supply Chain Analytics Dashboard</p>
<p style="font-size:13px;color:#5f6368;margin:2px 0 20px 0">AI Agent · BigQuery · dbt · Vertex AI</p>
""", unsafe_allow_html=True)

# ─── KPIs ─────────────────────────────────────────────────────────────────────
kpis = None
try:
    with st.spinner("Carregando KPIs..."):
        kpis = get_kpis()
    k = kpis.iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Lead Time Medio</div><div class="kpi-value">{k["avg_lead_time_days"]:.1f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">On-Time Delivery %</div><div class="kpi-value">{k["on_time_delivery_rate"]:.2f}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Receita Total</div><div class="kpi-value">{k["total_revenue"]:,.0f}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total de Pedidos</div><div class="kpi-value">{int(k["total_orders"]):,}</div></div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Erro KPIs: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Operational Performance ──────────────────────────────────────────────────
st.markdown('<p class="section-header">Operational Performance</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])
with col1:
    try:
        df = get_orders_by_month()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["mes"], y=df["total_pedidos"],
            mode="lines+markers", line=dict(color=BLUE, width=2),
            marker=dict(color=BLUE, size=5),
            fill="tozeroy", fillcolor="rgba(26,115,232,0.08)"))
        fig.update_layout(**plotly_base("Quantidade de Pedidos ao longo do tempo", 280))
        fig.update_xaxes(showgrid=True, gridcolor="#f1f3f4")
        fig.update_yaxes(showgrid=True, gridcolor="#f1f3f4")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(str(e))

with col2:
    try:
        df = get_revenue_by_country()
        fig = px.bar(df, x="pedidos", y="pais", orientation="h",
                     color_discrete_sequence=[BLUE], text="pedidos")
        fig.update_traces(textposition="outside")
        fig.update_layout(**plotly_base("Nr de Pedidos por Pais", 280))
        fig.update_yaxes(autorange="reversed", showgrid=False)
        fig.update_xaxes(showgrid=True, gridcolor="#f1f3f4")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(str(e))

col3, col4 = st.columns([2, 3])
with col3:
    try:
        df = get_scatter_data()
        fig = px.scatter(df, x="lead_time", y="receita", size="pedidos",
                         hover_name="pais", color_discrete_sequence=[BLUE])
        fig.update_layout(**plotly_base("Lead Time vs Receita por Pais", 300))
        fig.update_xaxes(title="Lead Time Medio (dias)", showgrid=True, gridcolor="#f1f3f4")
        fig.update_yaxes(title="Receita Total", showgrid=True, gridcolor="#f1f3f4")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(str(e))

with col4:
    try:
        df = get_revenue_by_country()
        fig = go.Figure(data=[go.Table(
            header=dict(values=["Pais", "Pedidos", "Receita", "Lead Time"],
                fill_color=BLUE, font=dict(color="white", size=12),
                align="left", height=32),
            cells=dict(values=[df["pais"], df["pedidos"], df["receita"], df["lead_time_medio"]],
                fill_color=[["#f8f9fa","white"]*10],
                align="left", height=28, font=dict(size=12))
        )])
        fig.update_layout(margin=dict(l=0,r=0,t=40,b=0), height=300,
                          paper_bgcolor="white",
                          title=dict(text="Performance por Pais", font=dict(size=13), x=0))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(str(e))

st.markdown("<br>", unsafe_allow_html=True)

# ─── Product Analysis ─────────────────────────────────────────────────────────
st.markdown('<p class="section-header">Product Analysis</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    try:
        df = get_revenue_by_category()
        fig = px.bar(df, x="receita", y="categoria", orientation="h",
                     color_discrete_sequence=[BLUE], text="receita")
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(**plotly_base("Receita por Categoria", 360))
        fig.update_yaxes(autorange="reversed", showgrid=False)
        fig.update_xaxes(showgrid=True, gridcolor="#f1f3f4")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(str(e))

with col6:
    try:
        df = get_revenue_by_brand()
        fig = px.bar(df, x="receita", y="marca", orientation="h",
                     color_discrete_sequence=[BLUE], text="receita")
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(**plotly_base("Receita por Marca", 360))
        fig.update_yaxes(autorange="reversed", showgrid=False)
        fig.update_xaxes(showgrid=True, gridcolor="#f1f3f4")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(str(e))

try:
    df = get_revenue_by_country()
    fig = px.treemap(df, path=["pais"], values="receita",
                     color="receita", color_continuous_scale=["#e8f0fe", BLUE])
    fig.update_layout(margin=dict(l=0,r=0,t=40,b=0), height=280,
                      paper_bgcolor="white",
                      title=dict(text="Receita por Pais", font=dict(size=13), x=0))
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(str(e))

st.markdown("<br>", unsafe_allow_html=True)

# ─── Chat ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">Converse com os Dados</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.messages:
    html = '<div class="chat-box">'
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            html += f'<div class="msg-lbl">Voce</div><div class="msg-user">{msg["content"]}</div>'
        else:
            lbl = "Gemini 2.5 Flash" if msg.get("model") == "gemini" else "Claude Opus 4.8"
            html += f'<div class="msg-lbl">{lbl}</div><div class="msg-agent">{msg["content"]}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

default_q = st.session_state.pop("suggested_question", "")
question = st.chat_input("Faca uma pergunta sobre Supply Chain...")

if question or default_q:
    q = question or default_q
    st.session_state.messages.append({"role": "user", "content": q})
    with st.spinner(f"{'Gemini' if model_choice == 'gemini' else 'Claude'} analisando..."):
        try:
            context = kpis.T.to_string() if kpis is not None else ""
            response = ask_agent(q, context, model=model_choice)
            st.session_state.messages.append({"role": "agent", "content": response, "model": model_choice})
            st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")

if st.session_state.messages:
    if st.button("Limpar conversa"):
        st.session_state.messages = []
        st.rerun()
