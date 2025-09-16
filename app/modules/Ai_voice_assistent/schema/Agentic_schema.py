from pydantic import BaseModel, Field



class AgentPayload(BaseModel):
    query: str