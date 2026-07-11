from fastapi import APIRouter
from api.models.schemas import AssistantInput, AssistantOutput
from Services.ragservice import ask_assistant

router = APIRouter()

@router.post("/ask-assistant", response_model=AssistantOutput)
def ask_assistant_endpoint(input: AssistantInput):
    result = ask_assistant(input.question)
    return AssistantOutput(
        answer=result["answer"],
        sources=result["sources"]
    )