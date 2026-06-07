#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import requests
import plotly.express as px

API = "https://ds-capstone-project.onrender.com"

@st.cache_data
def fetch(endpoint):
    response = requests.get(f"{API}{endpoint}")
    return response.json()

st.title("📊 Overview Dashboard")
st.caption("USA Federal IT Spending Analysis | 2016–2026")
st.divider()

summary = fetch("/summary")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Net IT Spend", f"${summary['net_spend_B']}B")
with col2:
    st.metric("Obligations", f"${summary['total_obligations_B']}B")
with col3:
    st.metric("Federal Agencies", f"{summary['total_agencies']}")
with col4:
    st.metric("Vendors", f"{summary['total_vendors']:,}")
with col5:
    st.metric("Peak Year", f"{summary['peak_year']}", f"${summary['peak_year_spend_B']}B")

st.caption(
    f"Data: {summary['date_from']} to {summary['date_to']} "
    f"| {summary['total_transactions']:,} transactions "
    f"| {summary['total_psc']} PSC categories"
)
st.divider()

st.subheader("📈 Annual Net Spend (2016–2025)")
annual = fetch("/annual-spend")

fig_annual = px.line(
    x=annual["years"],
    y=annual["spend"],
    labels={"x": "Year", "y": "Net Spend ($B)"},
    markers=True,
    color_discrete_sequence=["#378ADD"]
)
fig_annual.update_traces(
    line=dict(width=2.5),
    marker=dict(size=8)
)
fig_annual.update_layout(
    hovermode="x unified",
    plot_bgcolor="white",
    yaxis=dict(gridcolor="#f0f0f0"),
    xaxis=dict(gridcolor="#f0f0f0")
)
st.plotly_chart(fig_annual, use_container_width=True)
st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏢 Top 10 Agencies by Net Spend")
    agencies = fetch("/top-agencies")
    fig_agencies = px.bar(
        x=agencies["spend"],
        y=agencies["agencies"],
        orientation="h",
        labels={"x": "Net Spend ($B)", "y": ""},
        color_discrete_sequence=["#378ADD"]
    )
    fig_agencies.update_layout(
        plot_bgcolor="white",
        xaxis=dict(gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig_agencies, use_container_width=True)

with col_right:
    st.subheader("💻 Spend by Technology Group")
    categories = fetch("/category-spend")
    fig_cat = px.bar(
        x=categories["groups"],
        y=categories["spend"],
        labels={"x": "", "y": "Gross Spend ($B)"},
        color=categories["groups"],
        color_discrete_map={
            "IT Labour": "#378ADD",
            "New Tech":  "#1ac938",
            "Old Tech":  "#e8000b"
        }
    )
    fig_cat.update_layout(
        plot_bgcolor="white",
        showlegend=False,
        yaxis=dict(gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig_cat, use_container_width=True)


# In[ ]:




