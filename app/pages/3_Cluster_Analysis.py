#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

API = "https://ds-capstone-project.onrender.com"

@st.cache_data
def fetch(endpoint):
    response = requests.get(f"{API}{endpoint}")
    return response.json()

# ── Constants ────────────────────────────────────────────
CLUSTER_COLORS = {
    0: "#378ADD",
    1: "#e8000b",
    2: "#FF9500",
    3: "#9B59B6"
}

CLUSTER_ICONS = {
    0: "⚖️",
    1: "🏚️",
    2: "🔒",
    3: "📅"
}

CLUSTER_KEY_STAT = {
    0: "Balanced procurement health — the federal benchmark",
    1: "Legacy spend 4× the dataset average",
    2: "Vendor HHI 6× the dataset average — near single-vendor dependency",
    3: "September spend 2.8× their monthly average"
}

CLUSTER_INTERPRETATIONS = {
    0: (
        "The **Mainstream IT Procurers** represent the largest "
        "and most balanced cluster. These 49 agencies demonstrate "
        "healthy procurement behaviour — competitive vendor markets, "
        "moderate SaaS adoption, and strong framework discipline. "
        "They serve as the benchmark against which other clusters "
        "are assessed."
    ),
    1: (
        "The **Legacy Burdened** agencies are trapped in technology "
        "debt. Despite exemplary procurement process discipline — "
        "the highest framework usage of any cluster — these 7 agencies "
        "allocate a disproportionate share of spend to legacy IT "
        "categories. Their challenge is not how they buy, but what "
        "they buy. Targeted modernisation investment is the solution."
    ),
    2: (
        "The **Concentrated & Contracting** cluster contains only "
        "3 agencies but presents the most urgent risk profile. "
        "Extreme vendor concentration, minimal framework usage, and "
        "shrinking budgets suggest these agencies are at risk of "
        "procurement capability collapse. Immediate structural "
        "intervention is recommended."
    ),
    3: (
        "The **September Rushers** concentrate a disproportionate "
        "share of their annual IT spend in September — the federal "
        "fiscal year-end. These 6 agencies show strong overall "
        "procurement health but suffer from reactive budget "
        "execution. The pattern suggests spending to budget "
        "rather than to need."
    )
}

CLUSTER_POLICY = {
    0: "Maintain current trajectory. Nudge toward higher SaaS adoption. Use as benchmark for other clusters.",
    1: "Technology Modernization Fund (TMF) investment candidates. Process is sound — technology needs upgrading.",
    2: "Urgent vendor diversification needed. Mandate framework contract adoption. Risk of procurement capability collapse.",
    3: "Procurement planning reform required. Introduce quarterly spend targets to reduce September dependency."
}

RADAR_LABELS = [
    "SaaS%", "Legacy%", "HHI",
    "Sept%", "Growth", "Framework%"
]

FEATURES = [
    "saas_pct", "legacy_pct", "vendor_hhi",
    "sept_spike", "growth_rate", "framework_pct"
]

# ── Page header ──────────────────────────────────────────
st.title("🗂️ Cluster Analysis")
st.caption(
    "Unsupervised machine learning reveals four distinct "
    "federal IT procurement archetypes | "
    "KMeans clustering (k=4) applied to 6 procurement features"
)
st.markdown(
    "Not all federal agencies procure IT the same way. "
    "By applying unsupervised machine learning to six key "
    "procurement features — SaaS adoption, legacy burden, "
    "vendor concentration, seasonal spending, growth rate, "
    "and framework discipline — we identified four distinct "
    "agency archetypes. Each cluster tells a different story "
    "about how agencies buy technology and what interventions "
    "they need."
)

with st.expander("⚙️ Methodology"):
    st.markdown("""
    **Algorithm:** KMeans Clustering (k=4)  
    **Features used (6):**
    - SaaS Adoption % — share of spend on cloud/SaaS categories
    - Legacy Burden % — share of spend on legacy IT categories
    - Vendor HHI — Herfindahl-Hirschman Index measuring vendor concentration
    - September Spike % — share of annual spend in September
    - Growth Rate — linear trend slope normalised by mean spend
    - Framework Discipline % — share of spend through framework contracts

    **Pre-processing:** Isolation Forest outlier removal → StandardScaler → PCA (4 components, 82.5% variance)  
    **k=4 chosen over k=3** for greater analytical interpretability despite slightly lower silhouette score (0.369 vs 0.411)  
    **All features computed on net spend** (obligations minus deobligations)
    """)

st.divider()

# ── Load cluster data ────────────────────────────────────
clusters_data = fetch("/clusters")
clusters      = clusters_data["clusters"]

# ── Section 1: Cluster overview cards ───────────────────
st.subheader("📋 Cluster Overview")

col0, col1, col2, col3 = st.columns(4)
cols = [col0, col1, col2, col3]

for i, cluster in enumerate(clusters):
    cid   = cluster["cluster_id"]
    color = CLUSTER_COLORS[cid]
    icon  = CLUSTER_ICONS[cid]

    with cols[i]:
        st.markdown(
            f"<div style='"
            f"background-color:{color}20;"
            f"border-left: 4px solid {color};"
            f"padding: 12px;"
            f"border-radius: 6px;"
            f"margin-bottom: 8px'>"
            f"<b>{icon} Cluster {cid}</b><br>"
            f"<b>{cluster['cluster_name']}</b><br>"
            f"<span style='font-size:0.85em'>"
            f"n = {cluster['n_agencies']} agencies</span><br>"
            f"<span style='font-size:0.8em;color:{color}'>"
            f"{CLUSTER_KEY_STAT[cid]}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

st.divider()

# ── Section 2: Cluster profiles (Technical) ─────────────
st.subheader("📡 Cluster Profiles — Procurement Radar")
st.caption(
    "Each radar shows the centroid (average) profile "
    "of that cluster across 6 procurement features. "
    "Outward = more of each feature."
)

col_left, col_right = st.columns(2)

for i, cluster in enumerate(clusters):
    cid    = cluster["cluster_id"]
    color  = CLUSTER_COLORS[cid]
    col    = col_left if i % 2 == 0 else col_right
    values = [cluster[f] for f in FEATURES]

    with col:
        st.markdown(
            f"**{CLUSTER_ICONS[cid]} Cluster {cid}: "
            f"{cluster['cluster_name']} "
            f"(n={cluster['n_agencies']})**"
        )

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=RADAR_LABELS + [RADAR_LABELS[0]],
            fill="toself",
            fillcolor=color,
            opacity=0.3,
            line=dict(color=color, width=2.5),
            name=cluster["cluster_name"]
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True)
            ),
            showlegend=False,
            height=320,
            margin=dict(l=40, r=40, t=30, b=30)
        )
        st.plotly_chart(
            fig_radar,
            use_container_width=True,
            key=f"radar_{cid}"
        )
        st.caption(CLUSTER_INTERPRETATIONS[cid])
        st.divider()

# ── Section 3: Cluster comparison (Non-Technical) ───────
st.subheader("📊 Cluster Comparison")
st.caption(
    "How do the four clusters differ across "
    "key procurement dimensions?"
)

comparison_rows = []
feature_display = {
    "saas_pct":      "SaaS Adoption (%)",
    "legacy_pct":    "Legacy Burden (%)",
    "vendor_hhi":    "Vendor HHI",
    "sept_spike":    "September Spike (%)",
    "growth_rate":   "Growth Rate",
    "framework_pct": "Framework Discipline (%)"
}

for feat, label in feature_display.items():
    row = {"Feature": label}
    for cluster in clusters:
        cid = cluster["cluster_id"]
        name = cluster["cluster_name"].replace(
            " & ", " &\n"
        )
        row[f"C{cid}: {cluster['cluster_name']}"] = round(
            cluster[feat], 2
        )
    comparison_rows.append(row)

comp_df = pd.DataFrame(comparison_rows)
st.dataframe(
    comp_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ── Section 4: Policy recommendations ───────────────────
st.subheader("💡 Policy Recommendations")

for cluster in clusters:
    cid   = cluster["cluster_id"]
    color = CLUSTER_COLORS[cid]
    icon  = CLUSTER_ICONS[cid]

    st.markdown(
        f"**{icon} Cluster {cid} — "
        f"{cluster['cluster_name']}**"
    )
    st.info(CLUSTER_POLICY[cid])

st.divider()

# ── Section 5: Agency lists ──────────────────────────────
st.subheader("🏢 Agencies by Cluster")
st.caption(
    "Expand each cluster to see which "
    "agencies belong to that archetype"
)

for cluster in clusters:
    cid   = cluster["cluster_id"]
    icon  = CLUSTER_ICONS[cid]

    with st.expander(
        f"{icon} Cluster {cid}: "
        f"{cluster['cluster_name']} "
        f"(n={cluster['n_agencies']})"
    ):
        cols = st.columns(2)
        agencies = sorted(cluster["agencies"])
        mid = len(agencies) // 2

        with cols[0]:
            for agency in agencies[:mid]:
                st.write(f"• {agency}")
        with cols[1]:
            for agency in agencies[mid:]:
                st.write(f"• {agency}")


# In[ ]:





# In[ ]:




