from fastapi import APIRouter
from app.modules.persona.api.persona_api import app as persona_router

router = APIRouter(prefix="/persona", tags=["Persona Module"]
                   )
router.include_router(persona_router)