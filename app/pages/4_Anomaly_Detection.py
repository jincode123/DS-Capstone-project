#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests
import plotly.express as px

API = "http://127.0.0.1:8002"

@st.cache_data
def fetch(endpoint):
    response = requests.get(f"{API}{endpoint}")
    return response.json()

st.title("⚠️ Anomaly Detection")
st.caption(
    "Cluster-aware anomaly detection — "
    "agencies behaving differently from their peers"
)
st.divider()

anomaly_data = fetch("/anomalies")

# ── Method description ───────────────────────────────────
st.info(
    f"**Method:** {anomaly_data['method']} | "
    f"**Anomalies detected:** {anomaly_data['total_anomalies']}"
)
st.divider()

# ── Distance chart ───────────────────────────────────────
st.subheader("📊 Distance from Cluster Centroid")
anomalies = anomaly_data["anomalies"]

fig_dist = px.bar(
    x=[a["distance"] for a in anomalies],
    y=[a["agency"][:45] for a in anomalies],
    orientation="h",
    color=[a["type"] for a in anomalies],
    color_discrete_map={
        "Positive": "#1ac938",
        "Negative": "#e8000b"
    },
    labels={"x": "Distance from centroid", "y": ""}
)
fig_dist.update_layout(
    plot_bgcolor="white",
    xaxis=dict(gridcolor="#f0f0f0"),
    showlegend=True
)
st.plotly_chart(fig_dist, use_container_width=True)
st.divider()

# ── Individual anomaly cards ─────────────────────────────
st.subheader("🔍 Anomaly Findings")

type_icons = {
    "Positive": "✅",
    "Negative": "⚠️"
}

for anomaly in anomaly_data["anomalies"]:
    icon = type_icons[anomaly["type"]]

    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(
                f"**{icon} {anomaly['agency']}**"
            )
            st.caption(f"Cluster: {anomaly['cluster']}")
        with col2:
            st.metric("Distance",
                      f"{anomaly['distance']}")
        with col3:
            st.markdown(f"**Type:** {anomaly['type']}")

        st.write(f"**Why flagged:** {anomaly['reason']}")
        st.write(f"**Insight:** {anomaly['insight']}")
        st.divider()


# In[ ]:




