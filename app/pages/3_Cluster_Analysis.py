#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

API = "http://127.0.0.1:8002"

@st.cache_data
def fetch(endpoint):
    response = requests.get(f"{API}{endpoint}")
    return response.json()

st.title("🗂️ Cluster Analysis")
st.caption("Four distinct federal IT procurement archetypes")
st.divider()

clusters_data = fetch("/clusters")
clusters = clusters_data["clusters"]

cluster_colors = {
    0: "#378ADD",
    1: "#e8000b",
    2: "#FF9500",
    3: "#9B59B6"
}

policy_recs = {
    0: "Maintain current trajectory. Nudge toward higher SaaS adoption. Use as benchmark for other clusters.",
    1: "Technology Modernization Fund (TMF) investment candidates. Process is sound — technology needs upgrading.",
    2: "Urgent vendor diversification needed. Mandate framework contract adoption. Risk of procurement capability collapse.",
    3: "Procurement planning reform required. Introduce quarterly spend targets to reduce September dependency."
}

# ── Summary table ────────────────────────────────────────
st.subheader("📊 Cluster Overview")
table_data = []
for c in clusters:
    table_data.append({
        "Cluster":    f"{c['cluster_id']}: {c['cluster_name']}",
        "Agencies":   c["n_agencies"],
        "SaaS%":      c["saas_pct"],
        "Legacy%":    c["legacy_pct"],
        "HHI":        c["vendor_hhi"],
        "Sept%":      c["sept_spike"],
        "Growth":     c["growth_rate"],
        "Framework%": c["framework_pct"]
    })
st.dataframe(
    pd.DataFrame(table_data),
    use_container_width=True,
    hide_index=True
)
st.divider()

# ── Individual cluster profiles ──────────────────────────
st.subheader("🔍 Cluster Profiles")
col1, col2 = st.columns(2)

for i, cluster in enumerate(clusters):
    col = col1 if i % 2 == 0 else col2
    color = cluster_colors[cluster["cluster_id"]]

    with col:
        st.markdown(
            f"### Cluster {cluster['cluster_id']}: "
            f"{cluster['cluster_name']} "
            f"(n={cluster['n_agencies']})"
        )

        features = [
            "saas_pct", "legacy_pct", "vendor_hhi",
            "sept_spike", "growth_rate", "framework_pct"
        ]
        labels = [
            "SaaS%", "Legacy%", "HHI",
            "Sept%", "Growth", "Framework%"
        ]
        values = [cluster[f] for f in features]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values, theta=labels,
            fill="toself", fillcolor=color,
            opacity=0.3,
            line=dict(color=color, width=2),
            name=cluster["cluster_name"]
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=False,
            height=300,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        st.info(
            f"**Policy:** "
            f"{policy_recs[cluster['cluster_id']]}"
        )

        with st.expander(
            f"View {cluster['n_agencies']} agencies"
        ):
            for agency in sorted(cluster["agencies"]):
                st.write(f"• {agency}")

        st.divider()


# In[ ]:




