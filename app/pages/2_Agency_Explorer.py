#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

API = "https://ds-capstone-project.onrender.com"

# ── Cache only static data ───────────────────────────────
@st.cache_data
def get_agencies():
    response = requests.get(f"{API}/agencies")
    return response.json()

# Dynamic — no cache, refreshes per agency
def get_agency_data(agency_name):
    encoded = requests.utils.quote(agency_name)
    response = requests.get(f"{API}/agency/{encoded}")
    return response.json()

@st.cache_data
def get_summary():
    response = requests.get(f"{API}/summary")
    return response.json()

# ── Cluster definitions ──────────────────────────────────
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
        "vendor concentration (HHI above 0.5) combined with minimal "
        "framework usage and shrinking budgets suggests procurement "
        "capability at risk. Urgent vendor diversification and "
        "framework adoption are recommended."
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

# ── Anomaly agencies ─────────────────────────────────────
ANOMALY_AGENCIES = {
    "Railroad Retirement Board": {
        "type": "Positive",
        "reason": "SaaS adoption 67.9% — hidden modernisation champion"
    },
    "Committee for Purchase from People Who Are Blind or Severely Disabled": {
        "type": "Negative",
        "reason": "Vendor HHI 0.49 — extreme concentration risk"
    },
    "District of Columbia Courts": {
        "type": "Negative",
        "reason": "Zero framework contract usage"
    },
    "Selective Service System": {
        "type": "Negative",
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
agencies_list = get_agencies()
selected_agency = st.selectbox(
    "Select Agency",
    agencies_list["agencies"],
    index=agencies_list["agencies"].index(
        "Department of Defense"
    ) if "Department of Defense" in agencies_list["agencies"]
    else 0
)

if selected_agency:
    # Load agency data fresh each time
    agency_data = get_agency_data(selected_agency)
    summary = get_summary()

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

        # ── Section 1: Spending trend + vendors ──────────
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("**Annual Net Spend Trend**")
            fig_trend = px.bar(
                x=agency_data["annual_years"],
                y=agency_data["annual_spend"],
                labels={
                    "x": "Year",
                    "y": "Net Spend ($B)"
                },
                color_discrete_sequence=["#378ADD"]
            )
            fig_trend.update_layout(
                plot_bgcolor="white",
                yaxis=dict(gridcolor="#f0f0f0")
            )
            st.plotly_chart(
                fig_trend, use_container_width=True
            )

        with col_right:
            st.markdown("**Top 10 Vendors by Net Spend**")
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
                fig_vendors, use_container_width=True
            )

        st.divider()

        # ── Section 2: Cluster profile ───────────────────
        if agency_data["cluster"]:
            cluster = agency_data["cluster"]
            cluster_id = cluster["cluster_id"]
            color = CLUSTER_COLORS.get(cluster_id, "#378ADD")

            st.subheader("🗂️ Cluster Profile")

            # Cluster badge
            st.markdown(
                f"**Archetype: {CLUSTER_NAMES[cluster_id]}**"
            )

            # Written interpretation
            st.markdown(
                CLUSTER_INTERPRETATIONS[cluster_id]
            )

            # Policy recommendation
            st.info(
                f"**💡 Policy Recommendation:** "
                f"{CLUSTER_POLICY[cluster_id]}"
            )

            st.divider()

            # Radar + metrics comparison
            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown("**Procurement Profile Radar**")
                st.caption(
                    "Outward = more of each feature | "
                    "Grey dashed = cluster average"
                )

                features = [
                    "saas_pct", "legacy_pct",
                    "vendor_hhi", "sept_spike",
                    "growth_rate", "framework_pct"
                ]
                labels = [
                    "SaaS%", "Legacy%", "HHI",
                    "Sept%", "Growth", "Framework%"
                ]
                values = [cluster[f] for f in features]

                # Get cluster averages from cluster data
                cluster_avg = {
                    0: [23.3, 5.5, 0.09, 21.3, 0.06, 80.1],
                    1: [11.6, 27.3, 0.18, 21.5, -0.02, 89.2],
                    2: [4.8, 1.6, 0.59, 6.0, -0.13, 10.3],
                    3: [8.9, 5.2, 0.34, 59.4, 0.10, 76.5]
                }

                fig_radar = go.Figure()

                # Cluster average (grey dashed)
                avg_vals = cluster_avg[cluster_id]
                fig_radar.add_trace(go.Scatterpolar(
                    r=avg_vals + [avg_vals[0]],
                    theta=labels + [labels[0]],
                    fill="none",
                    line=dict(
                        color="gray",
                        dash="dash",
                        width=1.5
                    ),
                    name="Cluster Average"
                ))

                # Agency profile
                fig_radar.add_trace(go.Scatterpolar(
                    r=values + [values[0]],
                    theta=labels + [labels[0]],
                    fill="toself",
                    fillcolor=color,
                    opacity=0.3,
                    line=dict(color=color, width=2.5),
                    name=selected_agency[:25]
                ))

                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True)
                    ),
                    showlegend=True,
                    height=400,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2
                    )
                )
                st.plotly_chart(
                    fig_radar, use_container_width=True
                )

            with col_right:
                st.markdown(
                    "**Feature Comparison vs Cluster Average**"
                )
                st.caption(
                    "How this agency compares to its "
                    "cluster peers"
                )

                avg_vals = cluster_avg[cluster_id]
                feature_labels = [
                    "SaaS Adoption (%)",
                    "Legacy Burden (%)",
                    "Vendor HHI",
                    "September Spike (%)",
                    "Growth Rate",
                    "Framework Discipline (%)"
                ]

                comparison_data = []
                for i, (feat, label) in enumerate(
                    zip(features, feature_labels)
                ):
                    agency_val = cluster[feat]
                    avg_val    = avg_vals[i]
                    diff = agency_val - avg_val
                    comparison_data.append({
                        "Feature":        label,
                        "This Agency":    round(agency_val, 2),
                        "Cluster Average":round(avg_val, 2),
                        "Difference":     round(diff, 2)
                    })

                comp_df = pd.DataFrame(comparison_data)

                # Style the difference column
                def colour_diff(val):
                    if val > 0:
                        return "color: #1ac938"
                    elif val < 0:
                        return "color: #e8000b"
                    return ""

                st.dataframe(
                    comp_df.style.applymap(
                        colour_diff,
                        subset=["Difference"]
                    ),
                    use_container_width=True,
                    hide_index=True
                )

        else:
            st.info(
                "This agency was excluded from clustering "
                "analysis as a statistical outlier — its "
                "procurement patterns are too extreme to "
                "form meaningful peer comparisons."
            )


# In[ ]:




