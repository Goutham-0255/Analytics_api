from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class EventModel(SQLModel, table=True):
    __tablename__ = "events"

    # Forcing autoincrement identity mapping for composite primary keys
    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True}
    )
    time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        primary_key=True
    )
    page: str = Field(index=True)
    user_agent: str | None = Field(default=None)
    duration: float | None = Field(default=0.0)
