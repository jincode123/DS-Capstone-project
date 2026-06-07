#!/usr/bin/env python
# coding: utf-8

# In[4]:


import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go

API = "https://ds-capstone-project.onrender.com"

@st.cache_data
def fetch(endpoint):
    response = requests.get(f"{API}{endpoint}")
    return response.json()

st.title("🔍 Agency Explorer")
st.caption("Select an agency to explore its procurement profile")
st.divider()

agencies_list = fetch("/agencies")
selected_agency = st.selectbox(
    "Select Agency",
    agencies_list["agencies"]
)

if selected_agency:
    encoded = requests.utils.quote(selected_agency)
    agency_data = fetch(f"/agency/{encoded}")

    if "error" in agency_data:
        st.error(agency_data["error"])
    else:
        st.subheader(f"📊 {selected_agency}")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Net Spend",
                      f"${agency_data['net_spend_B']}B")
        with col2:
            st.metric("Total Vendors",
                      f"{agency_data['total_vendors']:,}")
        with col3:
            st.metric("Transactions",
                      f"{agency_data['total_transactions']:,}")
        with col4:
            st.metric("Deobligation Rate",
                      f"{agency_data['deob_rate_pct']}%")

        st.divider()
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("📈 Annual Spend Trend")
            fig_trend = px.bar(
                x=agency_data["annual_years"],
                y=agency_data["annual_spend"],
                labels={"x": "Year",
                        "y": "Net Spend ($B)"},
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
            st.subheader("🏭 Top 10 Vendors")
            fig_vendors = px.bar(
                x=agency_data["vendor_spend"],
                y=agency_data["vendor_names"],
                orientation="h",
                labels={"x": "Net Spend ($B)", "y": ""},
                color_discrete_sequence=["#378ADD"]
            )
            fig_vendors.update_layout(
                plot_bgcolor="white",
                xaxis=dict(gridcolor="#f0f0f0")
            )
            st.plotly_chart(
                fig_vendors, use_container_width=True
            )

        if agency_data["cluster"]:
            st.divider()
            cluster = agency_data["cluster"]
            st.subheader("🗂️ Cluster Profile")

            cluster_colors = {
                0: "#378ADD", 1: "#e8000b",
                2: "#FF9500", 3: "#9B59B6"
            }
            color = cluster_colors.get(
                cluster["cluster_id"], "#378ADD"
            )

            st.markdown(
                f"**Cluster {cluster['cluster_id']}: "
                f"{cluster['cluster_name']}**"
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("SaaS Adoption",
                          f"{cluster['saas_pct']}%")
                st.metric("Legacy Burden",
                          f"{cluster['legacy_pct']}%")
            with col2:
                st.metric("Vendor HHI",
                          f"{cluster['vendor_hhi']}")
                st.metric("September Spike",
                          f"{cluster['sept_spike']}%")
            with col3:
                st.metric("Growth Rate",
                          f"{cluster['growth_rate']}")
                st.metric("Framework Discipline",
                          f"{cluster['framework_pct']}%")

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
                name=selected_agency[:30]
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=False,
                height=400
            )
            st.plotly_chart(
                fig_radar, use_container_width=True
            )
        else:
            st.info(
                "This agency was excluded from "
                "clustering analysis (statistical outlier)"
            )


# In[ ]:





# In[ ]:




