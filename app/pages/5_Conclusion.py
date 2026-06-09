#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st

# ── Page header ──────────────────────────────────────────
st.title("📝 Conclusion")
st.caption(
    "Summary of findings, policy implications, "
    "limitations, and future work"
)
st.divider()

# ── Section 1: What We Found ─────────────────────────────
st.subheader("🔍 What We Found")
st.markdown(
    "This project applied data science and machine learning "
    "to 825,963 federal IT procurement transactions sourced "
    "from USASpending.gov, covering $579.6 billion in net "
    "spend across 72 agencies from 2016 to 2026. "
    "Three analytical questions were posed — and three "
    "clear answers emerged."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "**📊 Finding 1 — The Landscape**\n\n"
        "Federal IT net spend grew from $40B to $70B "
        "between 2016 and 2024. New Tech grew 285% while "
        "Old Tech collapsed 83% — with the crossover in "
        "2021. September consistently spikes at 2.8× the "
        "monthly average, suggesting agencies spend to "
        "budget rather than to need."
    )

with col2:
    st.info(
        "**🗂️ Finding 2 — The Archetypes**\n\n"
        "Four distinct procurement archetypes exist. "
        "75% of agencies are healthy Mainstream Procurers. "
        "The remaining 25% fall into profiles carrying "
        "technology debt, vendor concentration risk, or "
        "seasonal spending discipline issues — each "
        "requiring a different policy response."
    )

with col3:
    st.info(
        "**⚠️ Finding 3 — The Outliers**\n\n"
        "Within the Mainstream cluster, anomaly detection "
        "surfaced both risk and opportunity. The Railroad "
        "Retirement Board is a hidden modernisation "
        "champion worth replicating. Three agencies show "
        "procurement process gaps that warrant closer "
        "attention from oversight bodies."
    )

st.divider()

# ── Section 2: Policy Implications ──────────────────────
st.subheader("💡 Policy Implications")

recommendations = [
    {
        "cluster": "Mainstream IT Procurers (n=49)",
        "icon":    "⚖️",
        "color":   "#378ADD",
        "action":  "Maintain and benchmark",
        "detail":  (
            "Use these agencies as benchmarks for peer "
            "learning. The Railroad Retirement Board's "
            "SaaS adoption model should be documented "
            "and shared across this cluster."
        )
    },
    {
        "cluster": "Legacy Burdened (n=7)",
        "icon":    "🏚️",
        "color":   "#e8000b",
        "action":  "Technology Modernization Fund investment",
        "detail":  (
            "These agencies know how to buy — the problem "
            "is what they are buying. Targeted TMF "
            "investment to retire legacy systems is the "
            "most efficient intervention available."
        )
    },
    {
        "cluster": "Concentrated & Contracting (n=3)",
        "icon":    "🔒",
        "color":   "#FF9500",
        "action":  "Urgent vendor diversification",
        "detail":  (
            "HHI above 0.5 signals near single-vendor "
            "dependency. Mandatory diversification targets "
            "and framework contract adoption should be "
            "implemented immediately."
        )
    },
    {
        "cluster": "September Rushers (n=6)",
        "icon":    "📅",
        "color":   "#9B59B6",
        "action":  "Procurement planning reform",
        "detail":  (
            "Quarterly spend targets and early-year "
            "planning requirements would reduce September "
            "concentration and improve procurement quality."
        )
    }
]

for rec in recommendations:
    color = rec["color"]
    st.markdown(
        f"<div style='"
        f"background-color:{color}15;"
        f"border-left: 4px solid {color};"
        f"padding: 12px;"
        f"border-radius: 6px;"
        f"margin-bottom: 12px'>"
        f"<b>{rec['icon']} {rec['cluster']}</b> — "
        f"<b>{rec['action']}</b><br>"
        f"<span style='font-size:0.9em'>"
        f"{rec['detail']}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

st.divider()

# ── Section 3: Limitations ───────────────────────────────
st.subheader("⚠️ Limitations")

col_left, col_right = st.columns(2)

with col_left:
    st.warning(
        "**📋 PSC Category Classification**\n\n"
        "Category groupings are based on keyword matching "
        "against PSC descriptions. Some transactions may "
        "be misclassified where descriptions are ambiguous. "
        "Manual validation confirmed reasonable accuracy "
        "but edge cases exist."
    )
    st.warning(
        "**🏢 Agency-Level Analysis Only**\n\n"
        "This analysis operates at the department level. "
        "Within large agencies like DoD, significant "
        "variation exists between sub-components that "
        "is masked by aggregation."
    )

with col_right:
    st.warning(
        "**🔢 Clustering Subjectivity**\n\n"
        "The choice of k=4 involves analytical judgement. "
        "k=4 was chosen for interpretability over k=3 "
        "(silhouette 0.369 vs 0.411). Different k values "
        "would produce different archetypes."
    )
    st.warning(
        "**⚡ Causality vs Correlation**\n\n"
        "This analysis identifies patterns — it does not "
        "establish causality. The September spike reflects "
        "fiscal year structure but cannot distinguish "
        "strategic from reactive spending without "
        "qualitative analysis."
    )

st.divider()

# ── Section 4: Future Work ───────────────────────────────
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

# ── Section 5: Closing Statement ────────────────────────
st.subheader("🎯 Closing Statement")
st.markdown(
    """
    Federal IT procurement is not just a financial story —
    it is a story about how government modernises and serves
    its citizens through technology. The $579.6 billion spent
    between 2016 and 2026 represents a decade of technology
    decisions across 72 agencies with different missions,
    constraints, and priorities.

    This project demonstrates that data science can surface
    actionable patterns from large-scale procurement data —
    identifying which agencies are leading, which are falling
    behind, and which need targeted intervention.

    The most important finding may be the simplest:
    **procurement behaviour is measurable, comparable,
    and improvable** — and the data to do so is already
    publicly available.
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




