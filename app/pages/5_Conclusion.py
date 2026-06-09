#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st

# ── Page header ──────────────────────────────────────────
st.title("📝 Conclusion")
st.divider()

# ── Closing Statement ────────────────────────────────────
st.subheader("💬 Closing Statement")
st.markdown(
    """
    When I started this project, I wanted to understand
    where billions of dollars in federal IT spending actually
    go — and whether data science could reveal patterns that
    are invisible in raw transaction data.

    What surprised me most was not the scale of the spending,
    but the diversity of behaviour beneath it. Agencies with
    similar budgets and missions procure technology in
    fundamentally different ways — and those differences are
    measurable, comparable, and actionable.

    The four procurement archetypes, the hidden modernisation
    champion, and the September spending pattern are not just
    analytical findings — they are starting points for
    conversations about how federal IT procurement can improve.

    Procurement behaviour is measurable. The data is publicly
    available. The insights are actionable. That is the core
    contribution of this project.
    """
)
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




