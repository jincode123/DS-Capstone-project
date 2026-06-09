#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st

# ── Page header ──────────────────────────────────────────
st.title("📝 Conclusion")
st.divider()

# ── Brief recap ──────────────────────────────────────────
st.subheader("🎯 Project Summary")
st.markdown(
    "This project applied data science and machine learning "
    "to 825,963 federal IT procurement transactions from "
    "USASpending.gov to answer three questions — how federal "
    "IT spending has evolved, what procurement archetypes "
    "exist across agencies, and which agencies stand out "
    "from their peers. The result is an interactive "
    "analytical platform that translates $579.6 billion "
    "of procurement data into evidence-based insights for "
    "policy makers and IT modernisation teams."
)

st.divider()

# ── Future Work ──────────────────────────────────────────
st.subheader("🚀 Future Work")

col_left, col_right = st.columns(2)

with col_left:
    st.success(
        "**📝 NLP on Transaction Descriptions**\n\n"
        "Applying NLP to free-text transaction descriptions "
        "would enable finer-grained technology categorisation "
        "— capturing emerging categories like AI/ML services "
        "and zero-trust security that PSC codes do not yet "
        "reflect."
    )
    st.success(
        "**📈 Time Series Forecasting**\n\n"
        "A forecasting model trained on 2016-2024 data "
        "could project agency-level IT spend through "
        "2027-2028, enabling budget planning support and "
        "early warning of agencies trending toward "
        "problematic procurement profiles."
    )

with col_right:
    st.success(
        "**🔄 Real-Time Data Pipeline**\n\n"
        "USASpending.gov updates monthly. An automated "
        "pipeline could refresh the dataset monthly, "
        "triggering re-clustering and anomaly detection "
        "to provide continuously updated procurement "
        "intelligence."
    )
    st.success(
        "**🏢 Sub-Agency Analysis**\n\n"
        "Breaking large agencies like DoD into component "
        "sub-agencies would reveal procurement variation "
        "currently masked by department-level aggregation "
        "— enabling more targeted policy interventions."
    )

st.divider()

# ── Closing Statement ────────────────────────────────────
st.subheader("💬 Closing Statement")
st.markdown(
    """
    Federal IT procurement is not just a financial story —
    it is a story about how government modernises and serves
    its citizens through technology.

    This project demonstrates that procurement behaviour
    is **measurable, comparable, and improvable** — and
    the data to do so is already publicly available.
    The analytical framework developed here provides a
    foundation for evidence-based procurement policy
    that goes beyond aggregate spend figures.
    """
)

st.markdown(
    "<div style='text-align:center; padding: 20px; "
    "color: gray; font-size: 0.85em'>"
    "Federal IT Procurement Analysis | 2016–2026 | "
    "Data sourced from USASpending.gov API | "
    "Built with FastAPI + Streamlit"
    "</div>",
    unsafe_allow_html=True
)


# In[ ]:




