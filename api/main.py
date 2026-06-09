#!/usr/bin/env python
# coding: utf-8

# In[5]:


from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routers import overview, agency, cluster, anomaly

app = FastAPI(
    title="Federal IT Procurement API",
    description="API for federal IT procurement capstone analysis",
    version="1.0"
)

# ── Paths ────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(BASE_DIR, "data")
CHARTS_DIR = os.path.join(DATA_DIR, "charts")

# ── Serve chart images as static files ──────────────────
app.mount(
    "/charts",
    StaticFiles(directory=CHARTS_DIR),
    name="charts"
)

# ── Load JSON helper ─────────────────────────────────────
def load_json(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return json.load(f)

# ── Load all data once at startup ────────────────────────
print("Loading all data...")
app.state.data = {
    "summary":              load_json("summary.json"),
    "annual_spend":         load_json("annual_spend.json"),
    "annual_by_category":   load_json("annual_by_category.json"),
    "top15_agencies":       load_json("top15_agencies.json"),
    "category_spend":       load_json("category_spend.json"),
    "top15_vendors":        load_json("top15_vendors.json"),
    "vendor_concentration": load_json("vendor_concentration.json"),
    "vendor_cumulative":    load_json("vendor_cumulative.json"),
    "contract_vehicles":    load_json("contract_vehicles.json"),
    "seasonal_spend":       load_json("seasonal_spend.json"),
    "cluster_data":         load_json("cluster_profiles.json"),
    "anomaly_data":         load_json("anomaly_results.json"),
    "agency_cluster":       load_json("agency_cluster.json"),
    "agency_profiles":      load_json("agency_profiles.json"),
}
print(f"✓ All data loaded — {len(app.state.data)} datasets")

# ── Register routers ─────────────────────────────────────
app.include_router(overview.router)
app.include_router(agency.router)
app.include_router(cluster.router)
app.include_router(anomaly.router)

# ── General endpoints ────────────────────────────────────
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

# ── HEAD endpoints for UptimeRobot free tier ─────────────
@app.head("/")
def home_head():
    return Response(status_code=200)

@app.head("/health")
def health_head():
    return Response(status_code=200)


# In[ ]:




