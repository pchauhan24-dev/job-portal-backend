# Job Portal Backend API

A FastAPI-based backend for a job portal with MongoDB integration and JWT authentication. The API supports two user roles:

- Candidate
- Employer

## Features

### Authentication
- User registration
- User login
- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt

### Employer Features
- Create jobs
- View all jobs
- View individual jobs
- Update own jobs
- Delete own jobs
- View applications for own jobs
- Update application status

### Candidate Features
- View all jobs
- Search jobs
- View individual jobs
- Apply for jobs
- Prevent duplicate applications
- View applied jobs
- Track application status

## Tech Stack
- Python
- FastAPI
- MongoDB
- PyMongo
- JWT
- Passlib
- Bcrypt
- Pydantic
- Uvicorn
- Python-dotenv

## Project Structure

```text
job-portal-backend/
├── app/
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── jobs.py
│   │   └── applications.py
│   ├── utils/
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── database.py
│   └── main.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── venv/
```

## API Endpoints

### Authentication
Method	Endpoint	Description
POST	/signup	Register a new user
POST	/login	Login and receive JWT token

### Jobs
Method	Endpoint	Access
POST	/jobs/	Employer
GET	/jobs/	Public
GET	/jobs/{job_id}	Public
PUT	/jobs/{job_id}	Employer
DELETE	/jobs/{job_id}	Employer

### Applications
Method	Endpoint	Access
POST	/apply/{job_id}	Candidate
GET	/my-applications	Candidate
GET	/job-applications	Employer
PUT	/job-applications/{application_id}/status	Employer

### Job Search
Jobs can be searched using:
GET /jobs/?search=Python
Search supports:
- Job title
- Company
- Location
- Description
- Requirements

Application Status
Applications can have the following statuses:
- Applied
- Shortlisted
- Rejected

Employers can update the status of applications for their own jobs.

## Authentication
Protected endpoints use JWT Bearer authentication.
After logging in, copy the returned access token and use the Authorize button in Swagger UI.

## Running the Project
1. Clone the repository
git clone <your-github-repository-url>
cd job-portal-backend
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment
Windows PowerShell:
.\venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Configure environment variables
Create a .env file:
MONGO_URI=your_mongodb_connection_string
DATABASE_NAME=job_portal
JWT_SECRET=your_secret_key
Do not upload .env to GitHub.
6. Start the server
uvicorn app.main:app --reload
7. Open Swagger UI
http://127.0.0.1:8000/docs

## API Documentation
FastAPI automatically provides interactive API documentation through Swagger UI.
Swagger:
http://127.0.0.1:8000/docs
OpenAPI:
http://127.0.0.1:8000/openapi.json

## Project Status
Completed:
- Authentication
- JWT authorization
- Candidate role
- Employer role
- Job management
- Job search
- Job applications
- Application status tracking
- Role-based access control
- MongoDB integration