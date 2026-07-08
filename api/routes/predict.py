from fastapi import APIRouter
from api.models.schemas import SalesInput, SalesOutput
from Services.mlservice import predictrevenue

router = APIRouter()

@router.post("/predict-sales", response_model=SalesOutput)
def predict_sales(input: SalesInput):
    features = {
        "monthrev": input.monthrev,
        "monthorderitemcount": input.monthorderitemcount,
        "monthordercount": input.monthordercount,
        "monthavgrevenue": input.monthavgrevenue,
        "monthnumber": input.monthnumber
    }
    predicted = predictrevenue(features)
    return SalesOutput(predicted_revenue=predicted)