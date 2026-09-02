"""
streamlit_app.py — Streamlit UI for SupplyGuard.

Calls backend/data_ingestion.py, backend/vector_store.py and backend/rag_chain.py
directly as Python functions — no FastAPI / uvicorn / HTTP layer. This is the new
entry point for Streamlit Community Cloud.

DEPLOY ON STREAMLIT CLOUD:
1. Put this file in the project ROOT (same level as run.py).
2. In Streamlit Cloud app settings, set "Main file path" to: streamlit_app.py
3. In App settings -> Secrets, add:
       GOOGLE_API_KEY = "your_key_here"
       WEATHER_API_KEY = "your_key_here"   # optional, mock data used if absent
4. Make sure "streamlit" is listed in requirements.txt (see note at bottom of chat).
"""

import os
import sys
from datetime import datetime

import streamlit as st

# ── Path setup so `backend.*` imports work regardless of CWD ────────────────
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Pull secrets (Streamlit Cloud's way of storing keys) into os.environ, so the
# existing backend code — which reads keys via os.getenv()/.env — works as-is.
try:
    for key in ("GOOGLE_API_KEY", "WEATHER_API_KEY"):
        if key in st.secrets and not os.getenv(key):
            os.environ[key] = st.secrets[key]
except Exception:
    pass  # no secrets.toml present (e.g. local run without secrets) — fine

st.set_page_config(page_title="SupplyGuard — AI Risk Intelligence", page_icon="🛡️", layout="wide")


# ── Heavy resources: build once, cached across reruns ────────────────────────
@st.cache_resource(show_spinner="Loading knowledge base (news, weather, history)...")
def init_system():
    from backend.data_ingestion import fetch_all_data
    from backend.vector_store import build_vector_store, load_vector_store
    from backend.rag_chain import RiskAssessmentChain, ScenarioGenerationChain, ChatChain

    os.makedirs(os.path.join(ROOT_DIR, "vector_store", "chroma_db"), exist_ok=True)

    data = None
    try:
        data = fetch_all_data()
        vectordb = build_vector_store(data)
    except Exception as e:
        st.warning(f"Could not build fresh vector store ({e}); trying existing one on disk.")
        vectordb = load_vector_store()

    return {
        "vectordb": vectordb,
        "data": data,
        "risk_chain": RiskAssessmentChain(vectordb),
        "scenario_chain": ScenarioGenerationChain(vectordb),
        "chat_chain": ChatChain(vectordb),
        "last_refresh": datetime.now().isoformat(),
    }


if not os.getenv("GOOGLE_API_KEY"):
    st.error(
        "GOOGLE_API_KEY is not set. Add it under **App settings → Secrets** in "
        "Streamlit Cloud as:\n\n```\nGOOGLE_API_KEY = \"your_key_here\"\n```"
    )
    st.stop()

system = init_system()

# ── Sidebar: company profile ─────────────────────────────────────────────────
st.sidebar.header("Company Profile")
company_name = st.sidebar.text_input("Company name", "My Company")
industry = st.sidebar.text_input("Industry", "Manufacturing")
regions = st.sidebar.text_input("Regions (comma-separated)", "Asia Pacific")
key_suppliers = st.sidebar.text_input("Key suppliers (comma-separated)", "China")
critical_inputs = st.sidebar.text_input("Critical inputs (comma-separated)", "semiconductors")

company_profile = {
    "name": company_name,
    "industry": industry,
    "regions": [r.strip() for r in regions.split(",") if r.strip()],
    "key_suppliers": [s.strip() for s in key_suppliers.split(",") if s.strip()],
    "critical_inputs": [c.strip() for c in critical_inputs.split(",") if c.strip()],
}

st.sidebar.divider()
st.sidebar.caption(f"Vector store last built: {system['last_refresh']}")
if st.sidebar.button("🔄 Refresh data"):
    init_system.clear()
    st.rerun()

st.title("🛡️ SupplyGuard — AI Risk Intelligence")

tab_assess, tab_scenario, tab_chat, tab_data = st.tabs(
    ["Risk Assessment", "Scenario Generator", "Chat Assistant", "Data Overview"]
)

# ── Tab 1: Risk assessment ────────────────────────────────────────────────────
with tab_assess:
    query = st.text_area("Risk query", "Assess current supply chain risks", height=80)
    if st.button("Run risk assessment", type="primary"):
        with st.spinner("Fetching real-time news & weather, then analyzing..."):
            from backend.data_ingestion import fetch_news_articles, fetch_weather_data

            realtime_news = fetch_news_articles(max_per_feed=5)
            realtime_weather = fetch_weather_data()
            realtime_data = {
                "news": realtime_news,
                "weather": realtime_weather,
                "fetch_timestamp": datetime.now().isoformat(),
            }
            result = system["risk_chain"].run(
                query=query,
                company_profile=company_profile,
                realtime_data=realtime_data,
            )

        if result.get("fallback"):
            st.warning("AI quota exceeded — showing a data-driven fallback assessment.")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Overall risk level", result.get("overall_risk_level", "N/A"))
            st.metric("Risk score", result.get("risk_score", "N/A"))
        with col2:
            st.write(result.get("executive_summary", ""))

        st.subheader("Identified risks")
        for r in result.get("identified_risks", []):
            with st.expander(f"[{r.get('severity', '?')}] {r.get('title', 'Untitled risk')}"):
                st.write(r.get("description", ""))
                st.caption(f"Impact: {r.get('potential_impact', '')}")
                st.caption(f"Evidence: {r.get('evidence', '')} (source: {r.get('data_source', '')})")

        st.subheader("Mitigation strategies")
        for m in result.get("mitigation_strategies", []):
            with st.expander(m.get("strategy", "Strategy")):
                for a in m.get("actions", []):
                    st.write(f"- {a}")
                st.caption(f"Timeline: {m.get('timeline', '')} · Cost: {m.get('cost_estimate', '')}")

        st.subheader("Early warning indicators")
        for i in result.get("early_warning_indicators", []):
            st.write(f"- {i}")

        with st.expander("Raw JSON response"):
            st.json(result)

# ── Tab 2: Scenario generator ─────────────────────────────────────────────────
with tab_scenario:
    c1, c2, c3 = st.columns(3)
    scenario_type = c1.selectbox(
        "Scenario type",
        ["natural_disaster", "geopolitical", "pandemic", "labor", "logistics"],
    )
    region = c2.text_input("Region", "Asia Pacific")
    industry_s = c3.text_input("Industry", "Electronics")

    if st.button("Generate scenarios", type="primary"):
        with st.spinner("Generating scenarios..."):
            result = system["scenario_chain"].run(
                scenario_type=scenario_type, region=region, industry=industry_s
            )
        if result.get("fallback"):
            st.warning("AI quota exceeded — showing scenarios from historical data.")
        for s in result.get("scenarios", []):
            title = f"{s.get('title')} (probability {s.get('probability_score')}/10, severity {s.get('severity_score')}/10)"
            with st.expander(title):
                st.write(s.get("narrative", ""))
                st.caption(f"Historical analog: {s.get('historical_analog', '')}")
                st.write("**Cascade effects:**")
                for e in s.get("cascade_effects", []):
                    st.write(f"- {e}")
                st.caption(
                    f"Estimated recovery: {s.get('estimated_recovery_days', '?')} days · "
                    f"Financial impact: ${s.get('financial_impact_usd_millions', '?')}M"
                )

# ── Tab 3: Chat assistant ─────────────────────────────────────────────────────
with tab_chat:
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    for role, msg in st.session_state.chat_messages:
        with st.chat_message(role):
            st.write(msg)

    if question := st.chat_input("Ask about supply chain risks..."):
        st.session_state.chat_messages.append(("user", question))
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = system["chat_chain"].run(question)
            st.write(answer)
        st.session_state.chat_messages.append(("assistant", answer))

# ── Tab 4: Data overview ──────────────────────────────────────────────────────
with tab_data:
    data = system.get("data")
    if not data:
        st.info("Using a previously persisted vector store; live counts unavailable until next refresh.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("News articles", len(data.get("news", [])))
        c2.metric("Weather readings", len(data.get("weather", [])))
        c3.metric("Historical events", len(data.get("historical", [])))

        severe = [w["city"] for w in data.get("weather", []) if w.get("is_severe")]
        if severe:
            st.warning(f"Severe weather currently reported in: {', '.join(severe)}")

        with st.expander("Raw news articles"):
            st.json(data.get("news", []))
        with st.expander("Raw weather data"):
            st.json(data.get("weather", []))