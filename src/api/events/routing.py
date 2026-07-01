from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func, text
from api.db.session import get_session
from .models import EventModel

router = APIRouter()


@router.get("/healthz")
def read_api_health():
    return {"status": "ok", "message": "The API is alive!"}


@router.post("/")
def create_event(payload: dict, session: Session = Depends(get_session)):
    db_obj = EventModel.model_validate(payload)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


@router.get("/")
def read_aggregations(
    interval: str = Query(
        default="1 day", description="Time interval like '1 hour' or '1 day'"),
    session: Session = Depends(get_session)
):
    # Uses native TimescaleDB time_bucket via raw SQL matching your interval string
    query = text(f"""
        SELECT time_bucket('{interval}', time) AS bucket, page, COUNT(*) AS count
        FROM events
        GROUP BY bucket, page
        ORDER BY bucket ASC;
    """)
    results = session.execute(query).fetchall()
    return [{"bucket": r[0], "page": r[1], "count": r[2]} for r in results]
