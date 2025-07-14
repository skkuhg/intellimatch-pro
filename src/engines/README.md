# IntelliMatch Pro - Matching and Search Engines

This directory contains the core business logic engines for job matching and candidate search.

## Engines

- `search_engine.py`: LinkedIn search integration using Tavily AI
- `matching_engine.py`: AI-powered compatibility scoring engine
- `analytics_engine.py`: Data analytics and insights generation
- `recommendation_engine.py`: Personalized recommendation system

## Features

### Search Engine
- Advanced LinkedIn profile and job search
- Multi-parameter query optimization
- Result enhancement and filtering
- Rate limiting and error handling

### Matching Engine  
- AI-powered compatibility scoring
- Multi-dimensional analysis (skills, experience, culture)
- Explainable AI recommendations
- Fallback scoring algorithms

### Analytics Engine
- Interactive dashboard generation
- Market trend analysis
- Skill gap identification
- Salary benchmarking

## Usage

```python
from src.engines.search_engine import LinkedInSearchEngine
from src.engines.matching_engine import MatchingEngine
from src.engines.analytics_engine import JobMatchingAnalytics

# Initialize engines
search = LinkedInSearchEngine(api_key)
matching = MatchingEngine()
analytics = JobMatchingAnalytics()

# Search and match
jobs = await search.search_jobs(job_seeker)
matches = await matching.calculate_compatibility(job_seeker, jobs)
dashboard = analytics.generate_dashboard(matches)
```