from fastapi import APIRouter, Query
from app.modules.Ai_voice_assistent.schema.Agentic_schema import AgentPayload
from app.modules.Ai_voice_assistent.services.mainservice import agentic_graph
v1 = APIRouter(prefix="/ai_voice_assitant", tags=["Ai Agent"])

@v1.post("/chat")
async def ai_voice_assitant(payload: AgentPayload):
    #LangGraph logic will be here
    query = payload.query
    agent = await agentic_graph(query)
    return {"response" : agent["response"]}
