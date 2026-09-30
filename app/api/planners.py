from fastapi import APIRouter, Depends, UploadFile, File, Form
from ..models.schemas import HomeRequest, PartyRequest, JewelryRequest
from ..services.recommendations import make
from .auth import current_user
import json
router=APIRouter(tags=["planners"])

@router.post("/generate-home")
def home(body:HomeRequest,user=Depends(current_user)): return make(user["id"],"home",body)
@router.post("/generate-party")
def party(body:PartyRequest,user=Depends(current_user)): return make(user["id"],"party",body)
@router.post("/generate-jewelry")
async def jewelry(budget:float=Form(...),occasion:str=Form("Wedding"),style:str=Form("Elegant"),outfit_color:str=Form(""),preferences:str=Form(""),outfit_image:UploadFile|None=File(default=None),user=Depends(current_user)):
    req=JewelryRequest(budget=budget,occasion=occasion,style=style,outfit_color=outfit_color or None,preferences=[x.strip() for x in preferences.split(",") if x.strip()])
    image_bytes=await outfit_image.read() if outfit_image else None
    return make(user["id"],"jewelry",req,image_bytes,outfit_image.content_type if outfit_image else None)
