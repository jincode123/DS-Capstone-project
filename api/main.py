#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from fastapi import FastAPI
import json
import os

app = FastAPI(
    title="Federal IT Procurement API",
    description="API for federal IT procurement capstone analysis",
    version="1.0"
)

# ── Paths ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ── Load all pre-computed JSON results ───────────────────
def load_json(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return json.load(f)

print("Loading pre-computed results...")
SUMMARY         = load_json("summary.json")
ANNUAL_SPEND    = load_json("annual_spend.json")
TOP_AGENCIES    = load_json("top_agencies.json")
CATEGORY_SPEND  = load_json("category_spend.json")
CLUSTER_DATA    = load_json("cluster_profiles.json")
ANOMALY_DATA    = load_json("anomaly_results.json")
AGENCY_CLUSTER  = load_json("agency_cluster.json")
AGENCY_PROFILES = load_json("agency_profiles.json")
print("✓ All data loaded from JSON files")
print(f"✓ {len(AGENCY_PROFILES)} agency profiles loaded")

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
# ════════════════════════════════════════════════════════

@app.get("/summary")
def get_summary():
    return SUMMARY

@app.get("/annual-spend")
def get_annual_spend():
    return ANNUAL_SPEND

@app.get("/top-agencies")
def get_top_agencies():
    return TOP_AGENCIES

@app.get("/category-spend")
def get_category_spend():
    return CATEGORY_SPEND

# ════════════════════════════════════════════════════════
# SECTION 3: AGENCY EXPLORER
# ════════════════════════════════════════════════════════

@app.get("/agencies")
def get_agencies():
    agencies = sorted(AGENCY_PROFILES.keys())
    return {"agencies": agencies}

@app.get("/agency/{agency_name}")
def get_agency(agency_name: str):
    if agency_name not in AGENCY_PROFILES:
        return {"error": f"Agency '{agency_name}' not found"}

    profile = AGENCY_PROFILES[agency_name].copy()
    profile["cluster"] = AGENCY_CLUSTER.get(agency_name, {})
    return profile

# ════════════════════════════════════════════════════════
# SECTION 4: CLUSTER ANALYSIS
# ════════════════════════════════════════════════════════

@app.get("/clusters")
def get_clusters():
    return CLUSTER_DATA

# ════════════════════════════════════════════════════════
# SECTION 5: ANOMALY DETECTION
# ════════════════════════════════════════════════════════

@app.get("/anomalies")
def get_anomalies():
    return ANOMALY_DATA

