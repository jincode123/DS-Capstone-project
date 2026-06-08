#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fastapi import APIRouter, Request

router = APIRouter(tags=["Agency Explorer"])

@router.get("/agencies")
def get_agencies(request: Request):
    profiles = request.app.state.data["agency_profiles"]
    agencies = sorted(profiles.keys())
    return {"agencies": agencies}

@router.get("/agency/{agency_name}")
def get_agency(agency_name: str, request: Request):
    profiles = request.app.state.data["agency_profiles"]
    agency_cluster = request.app.state.data["agency_cluster"]

    if agency_name not in profiles:
        return {"error": f"Agency '{agency_name}' not found"}

    profile = profiles[agency_name].copy()
    profile["cluster"] = agency_cluster.get(agency_name, {})
    return profile


# In[ ]:




