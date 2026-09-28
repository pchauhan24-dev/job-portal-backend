from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.database import applications_collection, jobs_collection
from app.utils.dependencies import require_candidate, require_employer
from app.schemas.application import ApplicationStatusUpdate


router = APIRouter(
    tags=["Applications"]
)


# Candidate: Apply for a job
@router.post("/apply/{job_id}")
def apply_for_job(
    job_id: str,
    current_user=Depends(require_candidate)
):
    # Validate job ID
    try:
        object_id = ObjectId(job_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID"
        )

    # Check whether the job exists
    job = jobs_collection.find_one(
        {"_id": object_id}
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Prevent duplicate application
    existing_application = applications_collection.find_one(
        {
            "job_id": job_id,
            "candidate_id": current_user["id"]
        }
    )

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="You have already applied for this job"
        )

    application_data = {
        "job_id": job_id,
        "candidate_id": current_user["id"],
        "status": "Applied",
        "applied_at": datetime.now(timezone.utc).isoformat()
    }

    result = applications_collection.insert_one(
        application_data
    )

    return {
        "message": "Application submitted successfully",
        "application_id": str(result.inserted_id),
        "status": "Applied"
    }


# Candidate: View their applications
@router.get("/my-applications")
def get_my_applications(
    current_user=Depends(require_candidate)
):
    applications = list(
        applications_collection.find(
            {"candidate_id": current_user["id"]}
        )
    )

    for application in applications:
        application["id"] = str(application["_id"])
        del application["_id"]

    return applications


# Employer: View applications for their jobs
@router.get("/job-applications")
def get_job_applications(
    current_user=Depends(require_employer)
):
    # Get jobs belonging to the logged-in employer
    jobs = list(
        jobs_collection.find(
            {"employer_id": current_user["id"]}
        )
    )

    job_ids = [str(job["_id"]) for job in jobs]

    # Employer has no jobs
    if not job_ids:
        return []

    # Get applications for those jobs
    applications = list(
        applications_collection.find(
            {"job_id": {"$in": job_ids}}
        )
    )

    for application in applications:
        application["id"] = str(application["_id"])
        del application["_id"]

    return applications


# Employer: Update application status
@router.put("/job-applications/{application_id}/status")
def update_application_status(
    application_id: str,
    status_data: ApplicationStatusUpdate,
    current_user=Depends(require_employer)
):
    # Validate application ID
    try:
        object_id = ObjectId(application_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid application ID"
        )

    # Find application
    application = applications_collection.find_one(
        {"_id": object_id}
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    # Find the job related to this application
    try:
        job_object_id = ObjectId(application["job_id"])
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID in application"
        )

    job = jobs_collection.find_one(
        {"_id": job_object_id}
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Make sure employer owns the job
    if job["employer_id"] != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only update applications for your own jobs"
        )

    # Update status
    applications_collection.update_one(
        {"_id": object_id},
        {"$set": {"status": status_data.status}}
    )

    return {
        "message": "Application status updated successfully",
        "application_id": application_id,
        "status": status_data.status
    }