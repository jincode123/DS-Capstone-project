#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fastapi import APIRouter, Request

router = APIRouter(tags=["Overview Dashboard"])

@router.get("/summary")
def get_summary(request: Request):
    return request.app.state.data["summary"]

@router.get("/annual-spend")
def get_annual_spend(request: Request):
    return request.app.state.data["annual_spend"]

@router.get("/annual-by-category")
def get_annual_by_category(request: Request):
    return request.app.state.data["annual_by_category"]

@router.get("/top-agencies")
def get_top_agencies(request: Request):
    return request.app.state.data["top15_agencies"]

@router.get("/category-spend")
def get_category_spend(request: Request):
    return request.app.state.data["category_spend"]

@router.get("/top-vendors")
def get_top_vendors(request: Request):
    return request.app.state.data["top15_vendors"]

@router.get("/vendor-concentration")
def get_vendor_concentration(request: Request):
    return request.app.state.data["vendor_concentration"]

@router.get("/vendor-cumulative")
def get_vendor_cumulative(request: Request):
    return request.app.state.data["vendor_cumulative"]

@router.get("/contract-vehicles")
def get_contract_vehicles(request: Request):
    return request.app.state.data["contract_vehicles"]

@router.get("/seasonal-spend")
def get_seasonal_spend(request: Request):
    return request.app.state.data["seasonal_spend"]


# In[ ]:




