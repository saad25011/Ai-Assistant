from fastapi import FastAPI
from app.modules.persona.schema.schema import personaSchema

app = FastAPI(title="Persona API", version="1.0.0"
)


@app.post("/persona/")
async def create_persona(persona: personaSchema):
    return {"message": "Persona created successfully", "persona": persona}
