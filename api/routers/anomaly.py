#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fastapi import APIRouter, Request

router = APIRouter(tags=["Anomaly Detection"])

@router.get("/anomalies")
def get_anomalies(request: Request):
    return request.app.state.data["anomaly_data"]


# In[ ]:




