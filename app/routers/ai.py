from fastapi import APIRouter
from app.dependencies import AIBizDep, UserIdDep

router = APIRouter(
    prefix="/ai",
    tags=["ai"],
)

@router.post("/chat")
async def chat(message: str, biz: AIBizDep, user_id: UserIdDep) -> str:
    return await biz.get_base_agent_response(message)