from fastapi import APIRouter

# Import all routers
from app.modules.Ai_voice_assistent.api.assistant import v1 as ai_voice_assistant_router    

router = APIRouter()


# Register routers
router.include_router(ai_voice_assistant_router)
