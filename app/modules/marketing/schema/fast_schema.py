from pydantic import BaseModel ,Field

class FastSchema(BaseModel):
    id : int
    status : str = Field(..., description="Status of the fast schema")