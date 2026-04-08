from datetime import datetime

from pydantic import BaseModel


class JobRead(BaseModel):
    id: str
    project_id: str | None = None
    job_type: str
    status: str
    payload_json: dict
    result_json: dict | None = None
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
