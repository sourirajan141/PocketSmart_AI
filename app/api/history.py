from fastapi import APIRouter, Depends
from .auth import current_user
from ..services.recommendations import history
router=APIRouter(tags=["history"])
@router.get("/history")
def get_history(user=Depends(current_user)): return {"items":history(user["id"])}
