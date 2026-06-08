#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fastapi import APIRouter, Request

router = APIRouter(tags=["Cluster Analysis"])

@router.get("/clusters")
def get_clusters(request: Request):
    return request.app.state.data["cluster_data"]


# In[ ]:




