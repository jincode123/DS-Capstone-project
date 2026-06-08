#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import requests

API = "https://ds-capstone-project.onrender.com"

@st.cache_data
def fetch(endpoint):
    response = requests.get(f"{API}{endpoint}")
    return response.json()

# ── Constants ────────────────────────────────────────────
ANOMALY_TYPES = {
    "Positive": {
        "icon":  "✅",
        "color": "#1ac938",
        "label": "Hidden Champion"
    },
    "Negative": {
        "icon":  "⚠️",
        "color": "#e8000b",
        "label": "Attention Required"
    }
}

# ── Page header ──────────────────────────────────────────
st.title("⚠️ Anomaly Detection")
st.caption(
    "Cluster-aware anomaly detection identifies agencies "
    "behaving differently from their procurement peers | "
    "All figures represent **net spend** "
    "(obligations minus deobligations)"
)
st.markdown(
    "Once agencies are grouped into clusters, we can identify "
    "those that behave unexpectedly within their own peer group. "
    "This cluster-aware approach is more meaningful than "
    "dataset-wide anomaly detection — it asks not 'is this agency "
    "unusual overall?' but 'is this agency unusual compared to "
    "agencies that procure similarly?'\n\n"
    "Anomaly detection surfaces two types of signal: "
    "**negative signals** where procurement patterns warrant "
    "closer attention, and **positive signals** where agencies "
    "are quietly outperforming their peers and deserve to be "
    "studied as models of good practice."
)

with st.expander("⚙️ Methodology"):
    st.markdown("""
    **Method:** Cluster-aware Euclidean distance from centroid  
    **Threshold:** Mean + 1.5σ within each cluster  
    **Scope:** Applied to Cluster 0 (Mainstream IT Procurers) 
    — the largest and most analytically meaningful cluster  

    For each agency in Cluster 0, we compute the Euclidean 
    distance from that agency's feature vector to the cluster 
    centroid in normalised 6-dimensional feature space. 
    Agencies exceeding the threshold are flagged as anomalies.

    **Why Cluster 0 only?**  
    Clusters 1, 2, and 3 are themselves defined by extreme 
    values on specific features — they are already anomalous 
    by design. Anomaly detection within the mainstream cluster 
    is where the most actionable and surprising findings emerge.

    **Note:** Transaction-level Isolation Forest (Option A) 
    was also evaluated but found to identify large transactions 
    rather than behavioural anomalies — less analytically 
    valuable for policy purposes.
    """)

st.divider()

# ── Load anomaly data ────────────────────────────────────
anomaly_data = fetch("/anomalies")
anomalies    = anomaly_data["anomalies"]

# ── Section 1: Headline metrics ──────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Anomalies Detected",
        anomaly_data["total_anomalies"]
    )
with col2:
    st.metric(
        "Positive Signals",
        sum(1 for a in anomalies if a["type"] == "Positive")
    )
with col3:
    st.metric(
        "Attention Required",
        sum(1 for a in anomalies if a["type"] == "Negative")
    )

st.divider()

# ── Section 2: Exact notebook chart ─────────────────────
st.subheader("📊 Cluster-Aware Anomaly Detection")
st.caption(
    "Left: Top 20 Cluster 0 agencies by distance from "
    "centroid — red bars exceed the anomaly threshold. "
    "Right: Radar comparison of anomaly agencies vs "
    "cluster average. "
    "Reproduced exactly from analysis notebooks."
)

st.image(
    f"{API}/charts/anomaly_detection.png",
    use_container_width=True
)

st.divider()

# ── Section 3: Individual anomaly findings ───────────────
st.subheader("🔍 Anomaly Findings")
st.markdown(
    "Each anomaly tells a different story. "
    "Understanding why an agency is flagged is more "
    "important than the flag itself."
)

for anomaly in anomalies:
    atype  = anomaly["type"]
    config = ANOMALY_TYPES[atype]
    icon   = config["icon"]
    color  = config["color"]
    label  = config["label"]

    st.markdown(
        f"<div style='"
        f"background-color:{color}15;"
        f"border-left: 4px solid {color};"
        f"padding: 16px;"
        f"border-radius: 6px;"
        f"margin-bottom: 16px'>"
        f"<b>{icon} {anomaly['agency']}</b>"
        f"<span style='float:right;"
        f"color:{color};font-size:0.85em'>"
        f"{label}</span><br>"
        f"<span style='font-size:0.85em;color:gray'>"
        f"Cluster: {anomaly['cluster']} | "
        f"Distance: {anomaly['distance']}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(f"**Why flagged:**")
        st.write(anomaly["reason"])
    with col_right:
        st.markdown(f"**Insight:**")
        st.write(anomaly["insight"])

    st.divider()

# ── Section 4: Key takeaways ─────────────────────────────
st.subheader("💡 Key Takeaways")

st.success(
    "**✅ Positive Signal — Hidden Champion:**\n\n"
    "The Railroad Retirement Board demonstrates that small "
    "agencies can achieve exceptional SaaS modernisation "
    "without large budgets. Its procurement approach deserves "
    "to be studied and replicated across the Mainstream cluster."
)

st.warning(
    "**⚠️ Process Outliers — Framework Gap:**\n\n"
    "District of Columbia Courts and Selective Service System "
    "conduct zero procurement through framework contracts — "
    "far below the cluster average of 80%. This is not "
    "necessarily a problem, but it warrants explanation. "
    "Unique legal jurisdictions or mission profiles may justify "
    "direct purchasing, but oversight bodies should verify."
)

st.error(
    "**⚠️ Concentration Risk — Vendor Dependency:**\n\n"
    "The Committee for Purchase has an HHI of 0.49 — "
    "nearly five times the cluster average. This level of "
    "vendor concentration creates significant supply chain "
    "risk. Immediate vendor diversification is recommended."
)


# In[ ]:




