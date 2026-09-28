from pydantic import BaseModel
from typing import Optional, Literal


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    salary: Optional[str] = None
    description: str
    requirements: str
    job_type: Literal["Full-time", "Part-time", "Internship"]


class JobResponse(BaseModel):
    id: str
    title: str
    company: str
    location: str
    salary: Optional[str] = None
    description: str
    requirements: str
    job_type: str
    employer_id: str
    posted_date: str


class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    job_type: Optional[Literal["Full-time", "Part-time", "Internship"]] = None