# IntelliMatch Pro - Data Models

This directory contains Pydantic models for structured data handling throughout the system.

## Models

- `job_seeker.py`: JobSeeker profile model
- `job_posting.py`: Job posting and requirements model  
- `candidate.py`: Candidate profile model
- `match_result.py`: Matching results and analytics model
- `workflow_state.py`: LangGraph workflow state model

## Usage

```python
from src.models.job_seeker import JobSeeker
from src.models.job_posting import JobPosting
from src.models.match_result import MatchResult

# Create job seeker
job_seeker = JobSeeker(
    skills=["Python", "Machine Learning"],
    experience_years=3,
    education_level="Bachelor's"
)

# Create job posting
job_posting = JobPosting(
    title="Data Scientist",
    company="TechCorp",
    required_skills=["Python", "Statistics"]
)
```