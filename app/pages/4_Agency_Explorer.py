#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go

API = "https://ds-capstone-project.onrender.com"

# ── Fetch functions ──────────────────────────────────────
@st.cache_data
def get_agencies():
    response = requests.get(f"{API}/agencies")
    return response.json()

@st.cache_data(ttl=0)
def get_agency_data(agency_name: str):
    encoded = requests.utils.quote(agency_name)
    response = requests.get(f"{API}/agency/{encoded}")
    return response.json()

# ── Constants ────────────────────────────────────────────
CLUSTER_NAMES = {
    0: "Mainstream IT Procurers",
    1: "Legacy Burdened",
    2: "Concentrated & Contracting",
    3: "September Rushers"
}

CLUSTER_COLORS = {
    0: "#378ADD",
    1: "#e8000b",
    2: "#FF9500",
    3: "#9B59B6"
}

CLUSTER_INTERPRETATIONS = {
    0: (
        "This agency sits within the **Mainstream IT Procurers** "
        "cluster — the largest group representing 75% of federal "
        "agencies. These agencies demonstrate balanced procurement "
        "health: competitive vendor relationships, moderate SaaS "
        "adoption, and structured framework usage. They represent "
        "the benchmark for federal IT procurement."
    ),
    1: (
        "This agency is classified as **Legacy Burdened** — one of "
        "seven agencies carrying significant technology debt. Despite "
        "strong procurement process discipline (high framework usage), "
        "these agencies allocate a disproportionate share of spend to "
        "legacy IT categories. They are prime candidates for "
        "Technology Modernization Fund (TMF) investment."
    ),
    2: (
        "This agency falls into the **Concentrated & Contracting** "
        "cluster — the most concerning procurement profile. Extreme "
        "vendor concentration combined with minimal framework usage "
        "and shrinking budgets suggests procurement capability at "
        "risk. Urgent vendor diversification and framework adoption "
        "are recommended."
    ),
    3: (
        "This agency is a **September Rusher** — one of six agencies "
        "that concentrate a disproportionate share of annual IT spend "
        "in September, the federal fiscal year-end. This pattern "
        "suggests spending to budget rather than to need. Procurement "
        "planning reform and quarterly spend targets are recommended."
    )
}

CLUSTER_POLICY = {
    0: "Maintain current trajectory. Focus on increasing SaaS adoption and vendor diversity.",
    1: "Priority candidate for Technology Modernization Fund (TMF) investment. Technology upgrade needed, not process reform.",
    2: "Urgent action required: mandate vendor diversification and framework contract adoption.",
    3: "Implement quarterly spend targets to smooth year-end spending concentration."
}

ANOMALY_AGENCIES = {
    "Railroad Retirement Board": {
        "type":   "Positive",
        "reason": "SaaS adoption 67.9% — hidden modernisation champion"
    },
    "Committee for Purchase from People Who Are Blind or Severely Disabled": {
        "type":   "Negative",
        "reason": "Vendor HHI 0.49 — extreme vendor concentration risk"
    },
    "District of Columbia Courts": {
        "type":   "Negative",
        "reason": "Zero framework contract usage"
    },
    "Selective Service System": {
        "type":   "Negative",
        "reason": "Zero framework contract usage"
    }
}

# ── Page header ──────────────────────────────────────────
st.title("🔍 Agency Explorer")
st.caption(
    "Explore the procurement profile of any federal agency | "
    "All figures represent **net spend** "
    "(obligations minus deobligations)"
)
st.markdown(
    "Select an agency from the dropdown below to explore its "
    "spending trends, vendor relationships, technology profile, "
    "and procurement archetype. Use this page to understand how "
    "individual agencies compare to their peers and the dataset "
    "as a whole."
)
st.divider()

# ── Agency dropdown ──────────────────────────────────────
agencies_list   = get_agencies()
selected_agency = st.selectbox(
    "Select Agency",
    agencies_list["agencies"],
    index=agencies_list["agencies"].index(
        "Department of Defense"
    ) if "Department of Defense" in agencies_list["agencies"]
    else 0
)

if selected_agency:
    agency_data = get_agency_data(selected_agency)

    if "error" in agency_data:
        st.error(agency_data["error"])
    else:
        st.subheader(f"📊 {selected_agency}")

        # ── Anomaly flag ─────────────────────────────────
        if selected_agency in ANOMALY_AGENCIES:
            anomaly = ANOMALY_AGENCIES[selected_agency]
            if anomaly["type"] == "Positive":
                st.success(
                    f"✅ **Cluster Anomaly — Positive Signal:** "
                    f"{anomaly['reason']}"
                )
            else:
                st.warning(
                    f"⚠️ **Cluster Anomaly — Attention Required:** "
                    f"{anomaly['reason']}"
                )

        # ── Headline metrics ─────────────────────────────
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Net Spend (2016-2026)",
                f"${agency_data['net_spend_B']}B"
            )
        with col2:
            st.metric(
                "Unique Vendors",
                f"{agency_data['total_vendors']:,}"
            )
        with col3:
            st.metric(
                "Total Transactions",
                f"{agency_data['total_transactions']:,}"
            )
        with col4:
            st.metric(
                "Deobligation Rate",
                f"{agency_data['deob_rate_pct']}%",
                help="Deobligations as % of obligations"
            )

        st.divider()

        # ── Section 1: Category trend + Vendors ─────────
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(
                "**Annual IT Procurement by Category**"
            )
            cat = agency_data.get(
                "annual_by_category", {}
            )

            if cat and len(cat.get("years", [])) > 0:
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Bar(
                    x=cat["years"],
                    y=cat["new_tech"],
                    name="New Tech",
                    marker_color="#1ac938"
                ))
                fig_trend.add_trace(go.Bar(
                    x=cat["years"],
                    y=cat["it_labour"],
                    name="IT Labour",
                    marker_color="#378ADD"
                ))
                fig_trend.add_trace(go.Bar(
                    x=cat["years"],
                    y=cat["old_tech"],
                    name="Old Tech",
                    marker_color="#e8000b"
                ))
                fig_trend.update_layout(
                    barmode="stack",
                    plot_bgcolor="white",
                    yaxis=dict(
                        gridcolor="#f0f0f0",
                        title="Net Spend ($B)"
                    ),
                    xaxis=dict(title="Year"),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02
                    )
                )
                st.plotly_chart(
                    fig_trend,
                    use_container_width=True,
                    key=f"trend_{selected_agency}"
                )
            else:
                st.info(
                    "Category data not available — "
                    "API is updating. Please refresh "
                    "in a moment."
                )

        with col_right:
            st.markdown(
                "**Top 10 Vendors by Net Spend**"
            )
            fig_vendors = px.bar(
                x=agency_data["vendor_spend"],
                y=agency_data["vendor_names"],
                orientation="h",
                labels={
                    "x": "Net Spend ($B)",
                    "y": ""
                },
                color_discrete_sequence=["#378ADD"]
            )
            fig_vendors.update_layout(
                plot_bgcolor="white",
                xaxis=dict(gridcolor="#f0f0f0")
            )
            st.plotly_chart(
                fig_vendors,
                use_container_width=True,
                key=f"vendors_{selected_agency}"
            )

        st.divider()

        # ── Section 2: Cluster profile ───────────────────
        if agency_data.get("cluster"):
            cluster    = agency_data["cluster"]
            cluster_id = cluster["cluster_id"]

            st.subheader("🗂️ Cluster Profile")
            st.markdown(
                f"**Archetype: "
                f"{CLUSTER_NAMES[cluster_id]}**"
            )
            st.markdown(
                CLUSTER_INTERPRETATIONS[cluster_id]
            )
            st.info(
                f"**💡 Policy Recommendation:** "
                f"{CLUSTER_POLICY[cluster_id]}"
            )

        else:
            st.info(
                "This agency was excluded from clustering "
                "analysis as a statistical outlier — its "
                "procurement patterns are too extreme to "
                "form meaningful peer comparisons."
            )


# In[ ]:




