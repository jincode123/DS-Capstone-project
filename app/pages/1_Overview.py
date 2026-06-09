#!/usr/bin/env python
# coding: utf-8

# In[7]:


import streamlit as st
import requests

API = "https://ds-capstone-project.onrender.com"

@st.cache_data
def fetch(endpoint):
    response = requests.get(f"{API}{endpoint}")
    return response.json()

# ── Page header ──────────────────────────────────────────
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
to procurement transactions to uncover hidden trends,
evaluate procurement discipline, and understand technology
transition strategies across federal agencies — providing
insights to support future decisions and improvements.

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
        "The crossover happened in **2021** — a structural "
        "shift in how the government buys IT."
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

# ── Section 1: Spending by Category ─────────────────────
st.subheader("💰 Spending by Category")
st.caption(
    "Left: overall category breakdown | "
    "Right: annual trend by category — "
    "showing technology transition over time"
)
st.image(
    f"{API}/charts/eda_category.png",
    use_container_width=True
)

st.divider()

# ── Section 2: Agency Spend + Vendor Concentration ──────
st.subheader("🏢 Agency Spend & Vendor Concentration")
st.caption(
    "Left: top 15 agencies by net spend | "
    "Right: vendor concentration (HHI) per agency — "
    "red = high concentration risk"
)
st.image(
    f"{API}/charts/eda_agency_vendor.png",
    use_container_width=True
)

st.divider()

# ── Section 3: Vendor Landscape ─────────────────────────
st.subheader("🏭 Vendor Landscape")
st.caption(
    "Left: top 15 vendors by spend | "
    "Right: cumulative market concentration curve"
)
st.image(
    f"{API}/charts/eda_vendor_landscape.png",
    use_container_width=True
)

st.divider()

# ── Section 4: How It Is Bought ──────────────────────────
st.subheader("📋 How It Is Bought")
st.caption(
    "Left: spend by contract vehicle type | "
    "Right: average transaction size by award type"
)
st.image(
    f"{API}/charts/eda_contract_vehicles.png",
    use_container_width=True
)

st.divider()

# ── Section 5: Seasonal Spending ─────────────────────────
st.subheader("📅 Seasonal Spending Patterns")
st.caption(
    "Left: average monthly spend — September peaks at "
    "2.8× monthly average | "
    "Right: September spend by year with spike ratio"
)
st.image(
    f"{API}/charts/eda_seasonal.png",
    use_container_width=True
)


# In[ ]:




