#!/usr/bin/env python
# coding: utf-8

# In[3]:


from fastapi import APIRouter, Request

router = APIRouter(tags=["Agency Explorer"])

FEATURES = [
    "saas_pct", "legacy_pct", "vendor_hhi",
    "sept_spike", "growth_rate", "framework_pct"
]

@router.get("/agencies")
def get_agencies(request: Request):
    profiles = request.app.state.data["agency_profiles"]
    agencies = sorted(profiles.keys())
    return {"agencies": agencies}

@router.get("/agency/{agency_name}")
def get_agency(agency_name: str, request: Request):
    profiles       = request.app.state.data["agency_profiles"]
    agency_cluster = request.app.state.data["agency_cluster"]

    if agency_name not in profiles:
        return {"error": f"Agency '{agency_name}' not found"}

    profile = profiles[agency_name].copy()

    # Add cluster info
    profile["cluster"] = agency_cluster.get(agency_name, {})

    # Add individual feature values
    profile["features"] = {
        feat: profile.get(feat, 0)
        for feat in FEATURES
    }

    # annual_by_category is already in profile
    # from agency_profiles.json — no extra work needed

    return profile


# In[ ]:




