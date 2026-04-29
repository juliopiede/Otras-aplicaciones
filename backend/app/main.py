from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.db import get_connection

app = FastAPI(title="Bittácora Licitaciones API", version="1.1.0")


class Tender(BaseModel):
    id: str
    title: str
    description: str
    cpv_code: Optional[str] = None
    score: int
    priority: str
    status: str
    budget: Decimal
    deadline_at: Optional[datetime] = None
    source_url: Optional[str] = None


class TenderListResponse(BaseModel):
    items: List[Tender]
    total: int


class TenderStatusUpdate(BaseModel):
    status: str


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
    <!doctype html>
    <html lang="es">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Bittácora Licitaciones</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 2rem; }
          table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
          th, td { border: 1px solid #ddd; padding: 8px; }
          th { background: #f5f5f5; }
        </style>
      </head>
      <body>
        <h1>Panel MVP — Licitaciones Bittácora</h1>
        <p>Vista rápida de oportunidades cargadas en la base de datos.</p>
        <table id="tenders">
          <thead>
            <tr><th>ID</th><th>Título</th><th>Score</th><th>Prioridad</th><th>Estado</th><th>Presupuesto</th></tr>
          </thead>
          <tbody></tbody>
        </table>
        <script>
          async function loadTenders() {
            const res = await fetch('/tenders?limit=20');
            const data = await res.json();
            const tbody = document.querySelector('#tenders tbody');
            tbody.innerHTML = '';
            data.items.forEach(item => {
              const row = document.createElement('tr');
              row.innerHTML = `<td>${item.id}</td><td>${item.title}</td><td>${item.score}</td><td>${item.priority}</td><td>${item.status}</td><td>${item.budget}</td>`;
              tbody.appendChild(row);
            });
          }
          loadTenders();
        </script>
      </body>
    </html>
    """


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/tenders", response_model=TenderListResponse)
async def list_tenders(
    status: Optional[str] = Query(default=None),
    priority: Optional[str] = Query(default=None),
    min_score: Optional[int] = Query(default=None, ge=0, le=100),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> TenderListResponse:
    conditions = []
    args = []

    if status:
        args.append(status)
        conditions.append(f"status = ${len(args)}")
    if priority:
        args.append(priority)
        conditions.append(f"priority = ${len(args)}")
    if min_score is not None:
        args.append(min_score)
        conditions.append(f"score >= ${len(args)}")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    args.extend([limit, offset])

    query = f"""
    SELECT id, title, description, cpv_code, score, priority, status, budget, deadline_at, source_url
    FROM tenders
    {where_clause}
    ORDER BY score DESC, created_at DESC
    LIMIT ${len(args)-1} OFFSET ${len(args)}
    """

    try:
        async with get_connection() as conn:
            rows = await conn.fetch(query, *args)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    items = [Tender(**dict(row)) for row in rows]
    return TenderListResponse(items=items, total=len(items))


@app.patch("/tenders/{tender_id}/status", response_model=Tender)
async def update_tender_status(tender_id: str, payload: TenderStatusUpdate) -> Tender:
    if payload.status not in {"Nueva", "En análisis", "Decidida", "Presentada"}:
        raise HTTPException(status_code=400, detail="Invalid status")

    query = """
    UPDATE tenders
    SET status = $2, updated_at = NOW()
    WHERE id = $1
    RETURNING id, title, description, cpv_code, score, priority, status, budget, deadline_at, source_url
    """
    try:
        async with get_connection() as conn:
            row = await conn.fetchrow(query, tender_id, payload.status)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    if row is None:
        raise HTTPException(status_code=404, detail="Tender not found")

    return Tender(**dict(row))
