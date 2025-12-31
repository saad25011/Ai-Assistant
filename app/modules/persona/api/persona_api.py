from fastapi import APIRouter
from app.modules.persona.schema.schema import personaSchema

app = APIRouter(title="Persona API", version="1.0.0"
)


@app.post("/persona/")
async def create_persona(persona: personaSchema):
    return {"message": "Persona created successfully", "persona": persona}
