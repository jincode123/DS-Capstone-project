#!/usr/bin/env python
# coding: utf-8

# In[2]:


from fastapi import FastAPI
import pandas as pd
import json
import os

app = FastAPI(
    title="Federal IT Procurement API",
    description="API for federal IT procurement capstone analysis",
    version="1.0"
)

# ── Paths ────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR      = os.path.join(BASE_DIR, "data")
RESEARCH_PATH = os.path.join(DATA_DIR, "research_df_final.parquet")
CLUSTER_PATH  = os.path.join(DATA_DIR, "agency_cluster.json")

# ── Load pre-computed JSON results ───────────────────────
def load_json(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return json.load(f)

print("Loading pre-computed results...")
SUMMARY        = load_json("summary.json")
ANNUAL_SPEND   = load_json("annual_spend.json")
TOP_AGENCIES   = load_json("top_agencies.json")
CATEGORY_SPEND = load_json("category_spend.json")
CLUSTER_DATA   = load_json("cluster_profiles.json")
ANOMALY_DATA   = load_json("anomaly_results.json")
AGENCY_CLUSTER = load_json("agency_cluster.json")
print("✓ Pre-computed results loaded")

# ── Load raw data for dynamic endpoints ──────────────────
print("Loading research data for Agency Explorer...")
df = pd.read_parquet(RESEARCH_PATH)
df["Action Date"] = pd.to_datetime(df["Action Date"])
df["year"]  = df["Action Date"].dt.year
df["month"] = df["Action Date"].dt.month
pos = df[df["Transaction Amount"] > 0]
neg = df[df["Transaction Amount"] < 0]
print(f"✓ Loaded {len(df):,} rows")

# ════════════════════════════════════════════════════════
# SECTION 1: GENERAL
# ════════════════════════════════════════════════════════

@app.get("/")
def home():
    return {
        "message": "Federal IT Procurement API",
        "status":  "running",
        "version": "1.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

# ════════════════════════════════════════════════════════
# SECTION 2: OVERVIEW DASHBOARD
# Pre-computed from EDA notebook — exact numbers
# ════════════════════════════════════════════════════════

@app.get("/summary")
def get_summary():
    """Headline metrics — pre-computed from EDA notebook"""
    return SUMMARY

@app.get("/annual-spend")
def get_annual_spend():
    """Annual net spend — pre-computed from EDA notebook"""
    return ANNUAL_SPEND

@app.get("/top-agencies")
def get_top_agencies():
    """Top 10 agencies — pre-computed from EDA notebook"""
    return TOP_AGENCIES

@app.get("/category-spend")
def get_category_spend():
    """Technology group spend — pre-computed from EDA notebook"""
    return CATEGORY_SPEND

# ════════════════════════════════════════════════════════
# SECTION 3: AGENCY EXPLORER
# Dynamic — queries live data per agency selection
# ════════════════════════════════════════════════════════

@app.get("/agencies")
def get_agencies():
    """List of all agencies for dropdown"""
    agencies = sorted(df["Awarding Agency"].unique().tolist())
    return {"agencies": agencies}

@app.get("/agency/{agency_name}")
def get_agency(agency_name: str):
    """Full profile for selected agency — live query"""
    agency_df  = df[df["Awarding Agency"] == agency_name]
    agency_pos = agency_df[agency_df["Transaction Amount"] > 0]
    agency_neg = agency_df[agency_df["Transaction Amount"] < 0]

    if len(agency_df) == 0:
        return {"error": f"Agency '{agency_name}' not found"}

    # Annual spend trend
    annual = (
        agency_df.groupby("year")["Transaction Amount"]
        .sum().reset_index()
    )

    # Top vendors
    top_vendors = (
        agency_pos.groupby("Recipient Name")
        ["Transaction Amount"]
        .sum()
        .nlargest(10)
        .sort_values()
        .reset_index()
    )

    # Deobligation rate
    deob_rate = 0
    if len(agency_pos) > 0 and agency_pos["Transaction Amount"].sum() > 0:
        deob_rate = round(
            agency_neg["Transaction Amount"].abs().sum() /
            agency_pos["Transaction Amount"].sum() * 100, 1
        )

    # Cluster info from pre-computed JSON
    cluster_info = AGENCY_CLUSTER.get(agency_name, {})

    return {
        "agency":            agency_name,
        "net_spend_B":       round(
            agency_df["Transaction Amount"].sum() / 1000, 2
        ),
        "total_obligations_B": round(
            agency_pos["Transaction Amount"].sum() / 1000, 2
        ),
        "total_vendors":     int(agency_pos["Recipient Name"].nunique()),
        "total_transactions":int(len(agency_df)),
        "deob_rate_pct":     deob_rate,
        "annual_years":      annual["year"].tolist(),
        "annual_spend":      (
            annual["Transaction Amount"] / 1000
        ).round(2).tolist(),
        "vendor_names":      top_vendors["Recipient Name"].tolist(),
        "vendor_spend":      (
            top_vendors["Transaction Amount"] / 1000
        ).round(2).tolist(),
        "cluster":           cluster_info
    }

# ════════════════════════════════════════════════════════
# SECTION 4: CLUSTER ANALYSIS
# Pre-computed from clustering notebook — exact results
# ════════════════════════════════════════════════════════

@app.get("/clusters")
def get_clusters():
    """Cluster profiles — pre-computed from clustering notebook"""
    return CLUSTER_DATA

# ════════════════════════════════════════════════════════
# SECTION 5: ANOMALY DETECTION
# Pre-computed from anomaly notebook — exact results
# ════════════════════════════════════════════════════════

@app.get("/anomalies")
def get_anomalies():
    """Anomaly results — pre-computed from anomaly notebook"""
    return ANOMALY_DATA


# In[ ]:




