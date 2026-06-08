#!/usr/bin/env python
# coding: utf-8

# In[6]:


import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go

API = "https://ds-capstone-project.onrender.com"

@st.cache_data
def fetch(endpoint):
    response = requests.get(f"{API}{endpoint}")
    return response.json()

# ── Page header ─────────────────────────────────────────
st.title("📊 Federal IT Procurement — Overview")
st.caption(
    "Source: USASpending.gov API | "
    "All figures represent **net spend** "
    "(obligations minus deobligations) | "
    "2016–2025"
)
st.divider()

# ── Project statement ────────────────────────────────────
st.subheader("About This Project")
st.markdown("""
Federal IT procurement represents one of the largest 
concentrations of technology spending in the world. 
This project applies data science and machine learning 
to procurement transactions sourced from USASpending.gov 
to uncover hidden trends, evaluate procurement discipline, 
and understand technology transition strategies across 
federal agencies — providing insights to support future 
decisions and improvements.

**Three analytical questions drive this work:**

**What does federal IT spending look like at scale?**  
Exploratory Data Analysis reveals how spending has evolved 
over time, which technology categories are growing and 
declining, how vendors are distributed across agencies, 
and whether agencies are spending strategically or 
reactively.

**Are there distinct types of procurement agencies?**  
Unsupervised machine learning identifies agency archetypes 
with meaningfully different modernisation profiles, vendor 
strategies, and procurement discipline — enabling targeted 
policy recommendations.

**Which agencies behave differently from their peers?**  
Cluster-aware anomaly detection surfaces agencies that 
stand out — either as hidden modernisation champions worth 
studying and replicating, or as outliers whose procurement 
processes warrant closer attention.

The result is an interactive analytical platform that 
translates raw procurement data into actionable insights 
for policy makers, oversight bodies, and IT modernisation 
teams.
""")

with st.expander("📋 About this dataset"):
    st.markdown("""
    **Data Source:** USASpending.gov API  
    **Raw transactions:** 2,216,266  
    **After quality filtering:** 825,963 transactions  

    Filtering removed:
    - Transactions under $10K (444,989 rows — 0.2% of spend)
    - Discontinued vendors pre-2020 (0.1% of spend)
    - Discontinued PSC codes pre-2020
    - Non-IT related transactions

    **Final dataset:** 825,963 rows | 
    72 agencies | 118 PSC categories | 
    18,886 vendors | 2016–2026
    """)

st.divider()

# ── Headline metrics ─────────────────────────────────────
summary = fetch("/summary")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(
        "Net IT Spend",
        f"${summary['net_spend_B']}B",
        help="Total obligations minus deobligations 2016-2026"
    )
with col2:
    st.metric(
        "Federal Agencies",
        f"{summary['total_agencies']}"
    )
with col3:
    st.metric(
        "Unique Vendors",
        f"{summary['total_vendors']:,}"
    )
with col4:
    st.metric(
        "PSC Categories",
        f"{summary['total_psc']}"
    )
with col5:
    st.metric(
        "Peak Year (Net)",
        f"{summary['peak_year']}",
        help="Year with highest net spend"
    )

st.divider()

# ── Key findings ─────────────────────────────────────────
st.subheader("🔍 Key Findings")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(
        "**📈 Technology Transition**\n\n"
        "New Tech spending surged while Old Tech collapsed. "
        "The crossover happened in **2021** — marking a "
        "structural shift in how the government buys IT."
    )
with col2:
    st.warning(
        "**🏭 Vendor Concentration**\n\n"
        "Federal IT spending is highly concentrated. "
        "A small number of vendors capture a "
        "disproportionate share of all obligations, "
        "raising questions about competition and "
        "modernisation agility."
    )
with col3:
    st.error(
        "**📅 Seasonal Spending**\n\n"
        "A significant spike occurs every September — "
        "the federal fiscal year-end. This pattern "
        "suggests agencies are spending to budget "
        "rather than to need."
    )
with col4:
    st.success(
        "**📋 Award Discipline**\n\n"
        "The majority of IT spend flows through "
        "framework contracts — Delivery Orders and "
        "BPA Calls — indicating strong structural "
        "procurement discipline across agencies."
    )

st.divider()

# ── Section 1: Spending Trends ───────────────────────────
st.subheader("💰 Spending Trends")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("**Annual Federal IT Net Spend**")
    annual = fetch("/annual-spend")
    fig1 = px.bar(
        x=annual["years"],
        y=annual["spend"],
        labels={"x": "Year", "y": "Net Spend ($B)"},
        color_discrete_sequence=["#378ADD"]
    )
    fig1.update_layout(
        plot_bgcolor="white",
        yaxis=dict(gridcolor="#f0f0f0"),
        showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.markdown("**Annual IT Procurement by Category**")
    cat_data = fetch("/annual-by-category")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=cat_data["years"],
        y=cat_data["new_tech"],
        name="New Tech",
        marker_color="#1ac938"
    ))
    fig2.add_trace(go.Bar(
        x=cat_data["years"],
        y=cat_data["it_labour"],
        name="IT Labour",
        marker_color="#378ADD"
    ))
    fig2.add_trace(go.Bar(
        x=cat_data["years"],
        y=cat_data["old_tech"],
        name="Old Tech",
        marker_color="#e8000b"
    ))
    fig2.update_layout(
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
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Section 2: Vendor Landscape ──────────────────────────
st.subheader("🏭 Vendor Landscape")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("**Top 15 IT Vendors by Spend**")
    vendors = fetch("/top-vendors")
    fig5 = px.bar(
        x=vendors["spend"],
        y=vendors["vendors"],
        orientation="h",
        labels={"x": "Gross Spend ($B)", "y": ""},
        color_discrete_sequence=["#9B59B6"]
    )
    fig5.update_layout(
        plot_bgcolor="white",
        xaxis=dict(gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig5, use_container_width=True)

with col_right:
    st.markdown("**Vendor Market Concentration**")
    st.caption(
        "Cumulative % of spend by vendor rank — "
        "shows how concentrated the market is"
    )
    cumulative = fetch("/vendor-cumulative")
    fig6 = px.line(
        x=cumulative["ranks"],
        y=cumulative["cumulative_pct"],
        labels={
            "x": "Number of Vendors",
            "y": "Cumulative % of Spend"
        },
        color_discrete_sequence=["#9B59B6"],
        markers=True
    )
    fig6.update_layout(
        plot_bgcolor="white",
        yaxis=dict(gridcolor="#f0f0f0"),
        xaxis=dict(gridcolor="#f0f0f0", type="log")
    )
    fig6.add_hline(
        y=50, line_dash="dash",
        line_color="gray",
        annotation_text="50% of spend"
    )
    fig6.add_hline(
        y=80, line_dash="dash",
        line_color="orange",
        annotation_text="80% of spend"
    )
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("**Vendor Concentration by Agency (HHI)**")
st.caption(
    "Herfindahl-Hirschman Index (HHI) measures vendor "
    "dependency per agency. "
    "Higher HHI = fewer vendors dominating spend. "
    "0.25+ indicates high concentration."
)
concentration = fetch("/vendor-concentration")
fig7 = px.bar(
    x=concentration["hhi"],
    y=concentration["agencies"],
    orientation="h",
    labels={"x": "Vendor HHI", "y": ""},
    color=concentration["hhi"],
    color_continuous_scale=[
        "#1ac938", "#378ADD", "#FF9500", "#e8000b"
    ]
)
fig7.update_layout(
    plot_bgcolor="white",
    xaxis=dict(gridcolor="#f0f0f0"),
    coloraxis_showscale=False
)
fig7.add_vline(
    x=0.25, line_dash="dash",
    line_color="red",
    annotation_text="Concentration threshold (0.25)"
)
st.plotly_chart(fig7, use_container_width=True)

st.divider()

# ── Section 3: How It Is Bought ──────────────────────────
st.subheader("📋 How It Is Bought")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("**Contract Vehicle Analysis**")
    st.caption(
        "Framework contracts (Delivery Orders + BPA Calls) "
        "dominate federal IT procurement — "
        "indicating strong award discipline"
    )
    vehicles = fetch("/contract-vehicles")
    fig8 = px.pie(
        names=vehicles["types"],
        values=vehicles["spend"],
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig8.update_traces(
        textposition="outside",
        textinfo="percent+label"
    )
    st.plotly_chart(fig8, use_container_width=True)

with col_right:
    st.markdown("**Seasonal Spending Patterns**")
    st.caption(
        "Monthly net spend aggregated across all years — "
        "September consistently peaks at 2.8× monthly average"
    )
    seasonal = fetch("/seasonal-spend")
    colors = [
        "#e8000b" if m == "Sep" else "#378ADD"
        for m in seasonal["months"]
    ]
    fig9 = px.bar(
        x=seasonal["months"],
        y=seasonal["spend"],
        labels={"x": "Month", "y": "Net Spend ($B)"},
    )
    fig9.update_traces(marker_color=colors)
    fig9.update_layout(
        plot_bgcolor="white",
        yaxis=dict(gridcolor="#f0f0f0")
    )
    fig9.add_annotation(
        x="Sep",
        y=max(seasonal["spend"]),
        text="FY Year-End<br>2.8× average",
        showarrow=True,
        arrowhead=2,
        font=dict(color="red"),
        yshift=10
    )
    st.plotly_chart(fig9, use_container_width=True)


# In[ ]:




