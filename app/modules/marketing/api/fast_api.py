from fastapi import APIRouter
from app.modules.marketing.schema.fast_schema import FastSchema
router = APIRouter(title="Marketing API", version="1.0.0"
                   
                )
@router.post("/status")
async def get_marketing_status(
    payload: FastSchema
):
    try:
        return {"status": "Marketing API is running",
                "resposne": payload}
    except Exception as e:
        return {"error": str(e)}