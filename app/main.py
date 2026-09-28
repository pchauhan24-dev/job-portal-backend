from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.jobs import router as jobs_router
from app.routes.applications import router as applications_router


app = FastAPI(
    title="Job Portal Backend API",
    description="Backend API for a job portal with Candidate and Employer roles",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(jobs_router)
app.include_router(applications_router)


@app.get("/")
def root():
    return {
        "message": "Job Portal Backend API is running"
    }