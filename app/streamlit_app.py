#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st

st.set_page_config(
    page_title="Federal IT Procurement",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ Federal IT Procurement Analysis")
st.caption("USA Federal IT Spending | 2016–2026")
st.divider()

st.markdown("""
Welcome to the Federal IT Procurement Dashboard.

Use the sidebar to navigate between pages:

- 📊 **Overview Dashboard** — Key metrics and spending trends
- 🔍 **Agency Explorer** — Explore individual agency profiles
- 🗂️ **Cluster Analysis** — Four agency procurement archetypes
- ⚠️ **Anomaly Detection** — Agencies behaving differently from peers
""")


# In[ ]:




