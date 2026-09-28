from datetime import datetime, timezone
import re

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from app.database import jobs_collection
from app.schemas.job import JobCreate, JobUpdate
from app.utils.dependencies import require_employer


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# Create a new job - Employer only
@router.post("/")
def create_job(
    job: JobCreate,
    current_user=Depends(require_employer)
):
    job_data = {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "salary": job.salary,
        "description": job.description,
        "requirements": job.requirements,
        "job_type": job.job_type,
        "employer_id": current_user["id"],
        "posted_date": datetime.now(timezone.utc).isoformat()
    }

    result = jobs_collection.insert_one(job_data)

    return {
        "message": "Job created successfully",
        "job_id": str(result.inserted_id)
    }


# Get all jobs / Search jobs - Public
@router.get("/")
def get_all_jobs(
    search: str | None = Query(
        default=None,
        description="Search by job title, company, location, description, or requirements"
    )
):
    query = {}

    if search:
        search_regex = {
            "$regex": re.escape(search),
            "$options": "i"
        }

        query = {
            "$or": [
                {"title": search_regex},
                {"company": search_regex},
                {"location": search_regex},
                {"description": search_regex},
                {"requirements": search_regex}
            ]
        }

    jobs = list(jobs_collection.find(query))

    for job in jobs:
        job["id"] = str(job["_id"])
        del job["_id"]

    return jobs


# Get a single job by ID - Public
@router.get("/{job_id}")
def get_job(job_id: str):
    try:
        object_id = ObjectId(job_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID"
        )

    job = jobs_collection.find_one(
        {"_id": object_id}
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    job["id"] = str(job["_id"])
    del job["_id"]

    return job


# Update a job - Employer only, owner only
@router.put("/{job_id}")
def update_job(
    job_id: str,
    job: JobUpdate,
    current_user=Depends(require_employer)
):
    try:
        object_id = ObjectId(job_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID"
        )

    existing_job = jobs_collection.find_one(
        {"_id": object_id}
    )

    if not existing_job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if existing_job["employer_id"] != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own jobs"
        )

    update_data = {
        key: value
        for key, value in job.model_dump().items()
        if value is not None
    }

    if update_data:
        jobs_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )

    return {
        "message": "Job updated successfully"
    }


# Delete a job - Employer only, owner only
@router.delete("/{job_id}")
def delete_job(
    job_id: str,
    current_user=Depends(require_employer)
):
    try:
        object_id = ObjectId(job_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID"
        )

    existing_job = jobs_collection.find_one(
        {"_id": object_id}
    )

    if not existing_job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if existing_job["employer_id"] != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own jobs"
        )

    jobs_collection.delete_one(
        {"_id": object_id}
    )

    return {
        "message": "Job deleted successfully"
    }