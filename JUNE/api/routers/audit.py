import asyncio
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/audit", tags=["audit"])


class AuditRiskRequest(BaseModel):
    agency: str
    program: str
    audit_type: str
    contract_value: Optional[float] = None
    description: str


class AuditRiskResponse(BaseModel):
    result: str


def answer_query_with_rag(query: str, mode: str = "audit") -> str:
    """
    Placeholder for the synchronous RAG query function.
    Replace this with the actual implementation that performs retrieval-augmented generation.
    """
    raise NotImplementedError("answer_query_with_rag must be implemented")


@router.post("/risk", response_model=AuditRiskResponse)
async def assess_audit_risk(req: AuditRiskRequest) -> AuditRiskResponse:
    query = (
        f"Audit risk assessment for {req.agency} - {req.program}. "
        f"Audit type: {req.audit_type}. "
        f"{'Contract value: ' + f'{req.contract_value:,.0f}. ' if req.contract_value else ''}"
        f"Scope: {req.description}"
    )

    # OPTIMIZATION: Use asyncio.to_thread to run the synchronous RAG function
    # in a separate thread, preventing it from blocking the event loop.
    try:
        result = await asyncio.to_thread(answer_query_with_rag, query, mode="audit")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return AuditRiskResponse(result=result)
