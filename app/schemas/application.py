from pydantic import BaseModel
from typing import Literal


class ApplicationStatusUpdate(BaseModel):
    status: Literal["Applied", "Shortlisted", "Rejected"]


class ApplicationResponse(BaseModel):
    id: str
    job_id: str
    candidate_id: str
    status: Literal["Applied", "Shortlisted", "Rejected"]
    applied_at: str