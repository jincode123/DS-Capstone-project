#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
        "Federal IT spending grew steadily from $40B to "
        "$70B net between 2016 and 2024, driven entirely "
        "by New Tech adoption. Old Tech collapsed 83% "
        "while New Tech grew 285%. The technology "
        "crossover happened in 2021 — a structural shift "
        "in how the government buys IT. September remains "
        "a persistent problem — spending 2.8× the monthly "
        "average — suggesting agencies spend to budget "
        "rather than to need."
    )

with col2:
    st.info(
        "**🗂️ Finding 2 — The Archetypes**\n\n"
        "Four distinct procurement archetypes exist within "
        "federal IT. The majority (75%) are Mainstream "
        "Procurers operating within healthy parameters. "
        "However, 15% of agencies are either Legacy "
        "Burdened or Concentrated — profiles that carry "
        "measurable modernisation debt and supply chain "
        "risk. Each archetype requires a different policy "
        "response."
    )

with col3:
    st.info(
        "**⚠️ Finding 3 — The Outliers**\n\n"
        "Within the Mainstream cluster, anomaly detection "
        "surfaced both risk and opportunity. The Railroad "
        "Retirement Board demonstrates that small agencies "
        "can achieve world-class SaaS adoption without "
        "large budgets — a model worth replicating. "
        "Three agencies show procurement process gaps "
        "that warrant closer attention from oversight "
        "bodies."
    )

st.divider()

# ── Section 2: Policy Implications ──────────────────────
st.subheader("💡 Policy Implications")
st.markdown(
    "The findings translate directly into targeted policy "
    "recommendations — not broad mandates, but specific "
    "actions for specific agency profiles."
)

recommendations = [
    {
        "cluster":  "Mainstream IT Procurers (n=49)",
        "icon":     "⚖️",
        "color":    "#378ADD",
        "action":   "Maintain and benchmark",
        "detail":   (
            "These agencies represent healthy federal IT "
            "procurement. Policy focus should be on nudging "
            "SaaS adoption higher and using these agencies "
            "as benchmarks for peer learning programmes. "
            "The Railroad Retirement Board's SaaS model "
            "should be documented and shared across this cluster."
        )
    },
    {
        "cluster":  "Legacy Burdened (n=7)",
        "icon":     "🏚️",
        "color":    "#e8000b",
        "action":   "Technology Modernization Fund investment",
        "detail":   (
            "These agencies have exemplary procurement "
            "discipline — they know how to buy. The problem "
            "is what they are buying. Targeted TMF investment "
            "to accelerate legacy system retirement is the "
            "most efficient intervention. Process reform is "
            "not needed here — technology investment is."
        )
    },
    {
        "cluster":  "Concentrated & Contracting (n=3)",
        "icon":     "🔒",
        "color":    "#FF9500",
        "action":   "Urgent vendor diversification",
        "detail":   (
            "With HHI above 0.5 and minimal framework usage, "
            "these agencies face both supply chain and "
            "procurement capability risk. Mandatory vendor "
            "diversification targets and framework contract "
            "adoption should be implemented immediately. "
            "Without intervention, these agencies risk "
            "complete dependency on single vendors."
        )
    },
    {
        "cluster":  "September Rushers (n=6)",
        "icon":     "📅",
        "color":    "#9B59B6",
        "action":   "Procurement planning reform",
        "detail":   (
            "Concentrating annual spend in a single month "
            "is a symptom of reactive budget execution. "
            "Quarterly spend targets, early-year procurement "
            "planning requirements, and multi-year contract "
            "strategies would smooth spending patterns and "
            "improve procurement quality across these agencies."
        )
    }
]

for rec in recommendations:
    color = rec["color"]
    st.markdown(
        f"<div style='"
        f"background-color:{color}15;"
        f"border-left: 4px solid {color};"
        f"padding: 16px;"
        f"border-radius: 6px;"
        f"margin-bottom: 16px'>"
        f"<b>{rec['icon']} {rec['cluster']}</b><br>"
        f"<b>Recommended action: {rec['action']}</b>"
        f"</div>",
        unsafe_allow_html=True
    )
    st.write(rec["detail"])
    st.divider()

# ── Section 3: Limitations ───────────────────────────────
st.subheader("⚠️ Limitations")
st.markdown(
    "Acknowledging what this analysis cannot tell us "
    "is as important as what it can."
)

col_left, col_right = st.columns(2)

with col_left:
    st.warning(
        "**📋 PSC Category Classification**\n\n"
        "The New Tech / Old Tech / IT Labour grouping "
        "is based on keyword matching against PSC "
        "descriptions. Some transactions may be "
        "misclassified where descriptions are ambiguous "
        "or non-standard. Manual validation of a sample "
        "confirmed reasonable accuracy but edge cases exist."
    )
    st.warning(
        "**🏢 Agency-Level Analysis Only**\n\n"
        "This analysis operates at the agency level. "
        "Within large agencies like DoD, significant "
        "variation exists between sub-components. "
        "Department-level findings may mask component-level "
        "procurement issues or successes."
    )
    st.warning(
        "**📅 Partial 2026 Data**\n\n"
        "The dataset includes transactions through "
        "May 2026 only. Annual figures for 2026 are "
        "excluded from trend analysis to avoid misleading "
        "comparisons with full-year data."
    )

with col_right:
    st.warning(
        "**🔢 Clustering Subjectivity**\n\n"
        "The choice of k=4 clusters involves analytical "
        "judgement. While k=4 was chosen for interpretability "
        "over k=3 (silhouette 0.369 vs 0.411), different "
        "k values would produce different archetypes. "
        "The cluster labels reflect our interpretation "
        "of the centroid profiles."
    )
    st.warning(
        "**🏭 Vendor Name Standardisation**\n\n"
        "Vendor names in USASpending.gov data are not "
        "fully standardised. The same vendor may appear "
        "under multiple name variants, causing "
        "underestimation of true vendor concentration "
        "in some cases. HHI figures should be treated "
        "as lower bounds."
    )
    st.warning(
        "**⚡ Causality vs Correlation**\n\n"
        "This analysis identifies patterns and associations "
        "— it does not establish causality. The September "
        "spike, for example, reflects fiscal year structure "
        "but cannot distinguish between strategic and "
        "reactive spending without transaction-level "
        "qualitative analysis."
    )

st.divider()

# ── Section 4: Future Work ───────────────────────────────
st.subheader("🚀 Future Work")
st.markdown(
    "Several analytical extensions would significantly "
    "enhance the depth and utility of this work."
)

future_items = [
    {
        "title": "📝 NLP on Transaction Descriptions",
        "detail": (
            "Applying natural language processing to the "
            "free-text transaction descriptions would enable "
            "finer-grained technology categorisation beyond "
            "PSC codes — capturing emerging technology "
            "categories that PSC codes do not yet reflect, "
            "such as AI/ML services and zero-trust security."
        )
    },
    {
        "title": "📈 Time Series Forecasting",
        "detail": (
            "A forecasting model (Prophet or SARIMA) trained "
            "on the 2016-2024 data could project agency-level "
            "IT spend through 2027-2028, enabling budget "
            "planning support and early warning of agencies "
            "trending toward problematic procurement profiles."
        )
    },
    {
        "title": "🔄 Real-Time Data Pipeline",
        "detail": (
            "USASpending.gov updates monthly. An automated "
            "pipeline using Apache Airflow or Prefect could "
            "refresh the dataset monthly, triggering "
            "re-clustering and anomaly detection to provide "
            "continuously updated procurement intelligence."
        )
    },
    {
        "title": "🏢 Sub-Agency Analysis",
        "detail": (
            "Breaking DoD and other large agencies into "
            "their component sub-agencies (Army, Navy, "
            "Air Force etc.) would reveal procurement "
            "variation within departments that is currently "
            "masked by department-level aggregation."
        )
    },
    {
        "title": "🌐 Cross-Government Benchmarking",
        "detail": (
            "Extending the analysis to include state-level "
            "IT procurement data, or international equivalents "
            "such as UK Crown Commercial Service spend data, "
            "would enable cross-jurisdiction benchmarking "
            "and identification of global best practices."
        )
    },
    {
        "title": "🤖 Supervised Classification",
        "detail": (
            "With additional labelled data on procurement "
            "outcomes (project success/failure, cost overruns, "
            "vendor performance), a supervised classifier "
            "could predict which procurement patterns are "
            "most likely to result in poor outcomes — "
            "moving from descriptive to predictive analytics."
        )
    }
]

col_left, col_right = st.columns(2)

for i, item in enumerate(future_items):
    col = col_left if i % 2 == 0 else col_right
    with col:
        st.success(f"**{item['title']}**\n\n{item['detail']}")

st.divider()

# ── Section 5: Closing statement ────────────────────────
st.subheader("🎯 Closing Statement")
st.markdown(
    """
    Federal IT procurement is not just a financial story —
    it is a story about how government modernises, how it
    manages risk, and how it serves its citizens through
    technology. The $579.6 billion spent between 2016 and
    2026 represents a decade of technology decisions made
    by 72 agencies operating under different constraints,
    missions, and leadership priorities.

    This project demonstrates that data science can cut
    through the complexity of large-scale procurement data
    to surface actionable patterns — identifying which
    agencies are quietly leading, which are falling behind,
    and which need targeted intervention. The four
    procurement archetypes identified through clustering,
    and the anomalies surfaced through cluster-aware
    detection, provide a foundation for evidence-based
    procurement policy that goes beyond aggregate spend
    figures.

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

