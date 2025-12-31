from pydantic import BaseModel, Field

class personaSchema(BaseModel):
    name: str = Field(..., description="The name of the persona")
    age: int = Field(..., description="The age of the persona")
    occupation: str = Field(..., description="The occupation of the persona")