from pydantic import BaseModel
 
class SalesInput(BaseModel):
    monthrev: float
    monthorderitemcount: int
    monthordercount: int
    monthavgrevenue: float
    monthnumber: int  
 
class SalesOutput(BaseModel):
    predicted_revenue: float
 
class AssistantInput(BaseModel):
    question: str
 
class AssistantOutput(BaseModel):
    answer: str
    sources: list[str]    