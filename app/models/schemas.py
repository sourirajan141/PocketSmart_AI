from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    rooms: List[str] = Field(min_length=1)
    style: str = "Modern"
    priorities: List[str] = []
    quantities: Dict[str, int] = {}

class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0, le=10000)
    event_type: str = "Birthday"
    venue: str = "Home"
    city: str = ""
    preferences: List[str] = []

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str = "Wedding"
    style: str = "Elegant"
    outfit_color: Optional[str] = None
    preferences: List[str] = []

class RecommendationResponse(BaseModel):
    planner: str
    budget: float
    summary: str
    allocation: Dict[str, float]
    recommendations: List[Dict[str, Any]]
    ai_used: bool = False
    note: str = ""
