GearGuard Backend
GearGuard is a maintenance and equipment management system built with FastAPI and SQLAlchemy. It provides a robust API for user authentication, equipment tracking, and maintenance request processing.

🚀 Features
User Authentication: Secure signup and login using JWT (JSON Web Tokens).

Equipment Tracking: Complete lifecycle management for assets including serial numbers, warranty info, and scrap logic.

Maintenance Requests: Formal request system with priority levels, scheduled dates, and status tracking.

CORS Enabled: Configured to work seamlessly with frontend applications.

Database Integration: Uses SQLite with SQLAlchemy for reliable data persistence.

🛠️ Tech Stack
Framework: FastAPI

Database: SQLite

ORM: SQLAlchemy 2.0

Validation: Pydantic

Security: Python-jose (JWT)

📋 Prerequisites
Ensure you have Python installed. It is recommended to use a virtual environment.

```Bash

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

⚙️ Installation
Install dependencies:

```bash

pip install -r requirment.txt
Initialize the Database: The system will automatically create the sqllite.db file and necessary tables upon the first run of the application.
```

🏃 Running the Application
Start the development server using Uvicorn:

```Bash

uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000. You can access the interactive API documentation at http://127.0.0.1:8000/docs.
```

📡 API Endpoints
Authentication
POST /signup/: Register a new user.

POST /login/: Authenticate and receive a JWT access token.

Dashboard
GET /dashboard: Protected route to fetch logged-in user profile details.

Equipment Management
POST /equipment/: Add new equipment to the system.

GET /view_equipment/: Retrieve a list of all registered equipment.

Maintenance Requests
POST /requestform/: Create a new maintenance request.

GET /view_requests/: Fetch all active maintenance requests.

📂 Project Structure
main.py: Main application entry point containing API routes and logic.

models.py: SQLAlchemy database models (User, Equipment, RequestForm, etc.).

database.py: Database engine and session configuration.

requirment.txt: List of necessary Python packages.
