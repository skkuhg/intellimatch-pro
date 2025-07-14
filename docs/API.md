# IntelliMatch Pro API Documentation

## Overview

IntelliMatch Pro provides a comprehensive API for AI-powered job matching and talent discovery. The API is built using LangChain and LangGraph frameworks, providing both synchronous and asynchronous interfaces.

## Core Components

### 1. Data Models

#### JobSeeker
```python
class JobSeeker(BaseModel):
    skills: List[str]
    experience_years: int
    education_level: str
    preferred_salary_range: Optional[str]
    preferred_location: Optional[str]
    preferred_job_types: List[str]
    career_goals: Optional[str]
```

#### JobPosting
```python
class JobPosting(BaseModel):
    title: str
    company: str
    location: str
    job_type: str
    salary_range: Optional[str]
    required_skills: List[str]
    experience_required: str
    education_required: str
    description: str
```

#### MatchResult
```python
class MatchResult(BaseModel):
    job_seeker_id: str
    job_posting_id: str
    compatibility_score: float
    explanation: str
    skill_match_percentage: float
    experience_fit: str
    salary_alignment: str
    recommendations: List[str]
```

### 2. Search Engine

#### LinkedInSearchEngine
```python
class LinkedInSearchEngine:
    def __init__(self, tavily_api_key: str)
    def search_jobs(self, job_seeker: JobSeeker) -> List[Dict]
    def search_candidates(self, job_posting: JobPosting) -> List[Dict]
    def enhance_search_results(self, results: List[Dict]) -> List[Dict]
```

**Methods:**
- `search_jobs()`: Find job opportunities for job seekers
- `search_candidates()`: Find candidates for job postings
- `enhance_search_results()`: Enrich search results with additional data

### 3. Matching Engine

#### MatchingEngine
```python
class MatchingEngine:
    def __init__(self, llm: ChatOpenAI)
    def calculate_job_compatibility(self, job_seeker: JobSeeker, job_posting: JobPosting) -> MatchResult
    def calculate_candidate_compatibility(self, candidate: Candidate, job_posting: JobPosting) -> MatchResult
    def generate_recommendations(self, match_results: List[MatchResult]) -> Dict
```

**Methods:**
- `calculate_job_compatibility()`: Score job-seeker compatibility
- `calculate_candidate_compatibility()`: Score candidate-job compatibility
- `generate_recommendations()`: Generate actionable recommendations

### 4. Workflow Engine

#### LangGraph Workflow
```python
def create_job_matching_workflow() -> CompiledStateGraph:
    # Creates a state-based workflow for job matching
    # Nodes: input_processing -> search -> enhancement -> matching -> recommendations
```

**Workflow Nodes:**
1. `process_user_input`: Parse and validate user input
2. `search_linkedin_profiles`: Search for jobs/candidates
3. `enhance_search_data`: Enrich search results
4. `calculate_matches`: Compute compatibility scores
5. `generate_recommendations`: Create final recommendations
6. `format_final_output`: Format results for display

### 5. Analytics Engine

#### JobMatchingAnalytics
```python
class JobMatchingAnalytics:
    def generate_job_seeker_dashboard(self, results: List[MatchResult]) -> go.Figure
    def generate_recruiter_dashboard(self, results: List[MatchResult]) -> go.Figure
    def create_compatibility_matrix(self, results: List[MatchResult]) -> go.Figure
    def analyze_skill_gaps(self, job_seeker: JobSeeker, jobs: List[JobPosting]) -> Dict
    def generate_market_insights(self, search_results: List[Dict]) -> Dict
```

## API Usage Examples

### Job Seeker Workflow

```python
# Initialize components
search_engine = LinkedInSearchEngine(tavily_api_key)
matching_engine = MatchingEngine(llm)
analytics = JobMatchingAnalytics()

# Create job seeker profile
job_seeker = JobSeeker(
    skills=["Python", "Machine Learning", "Data Analysis"],
    experience_years=3,
    education_level="Bachelor's",
    preferred_salary_range="$80,000 - $120,000",
    preferred_location="Remote",
    preferred_job_types=["Full-time"],
    career_goals="Transition to AI/ML engineering role"
)

# Run workflow
workflow = create_job_matching_workflow()
results = workflow.invoke({
    "request_type": "job_seeker",
    "user_input": job_seeker.dict()
})

# Generate analytics
dashboard = analytics.generate_job_seeker_dashboard(results["matches"])
```

### Recruiter Workflow

```python
# Create job posting
job_posting = JobPosting(
    title="Senior Data Scientist",
    company="TechCorp Inc.",
    location="San Francisco, CA",
    job_type="Full-time",
    salary_range="$130,000 - $180,000",
    required_skills=["Python", "TensorFlow", "Statistics"],
    experience_required="5+ years",
    education_required="Master's in related field",
    description="Leading data science projects..."
)

# Run workflow
results = workflow.invoke({
    "request_type": "recruiter",
    "user_input": job_posting.dict()
})

# Generate analytics
dashboard = analytics.generate_recruiter_dashboard(results["matches"])
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `TAVILY_API_KEY` | Tavily AI API key | Yes |
| `LANGCHAIN_API_KEY` | LangSmith API key | No |
| `LANGCHAIN_PROJECT` | LangSmith project name | No |
| `LANGCHAIN_TRACING_V2` | Enable tracing | No |

### LLM Configuration

```python
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    max_tokens=2000,
    timeout=30
)
```

### Search Configuration

```python
search_config = {
    "max_results": 100,
    "search_depth": "advanced",
    "include_inactive": False,
    "region": "global"
}
```

## Error Handling

### Common Error Codes

- `INVALID_API_KEY`: Invalid or missing API key
- `RATE_LIMIT_EXCEEDED`: API rate limit exceeded
- `INVALID_INPUT`: Invalid input parameters
- `SEARCH_FAILED`: Search operation failed
- `MATCHING_ERROR`: Matching calculation error
- `WORKFLOW_ERROR`: Workflow execution error

### Error Response Format

```python
{
    "error": {
        "code": "SEARCH_FAILED",
        "message": "Failed to search for candidates",
        "details": "Tavily API returned 429 - Rate limit exceeded",
        "timestamp": "2025-07-14T05:47:05Z"
    }
}
```

## Performance Considerations

### Rate Limits

- **OpenAI API**: 10,000 tokens/minute
- **Tavily API**: 1,000 requests/month (free tier)
- **Concurrent Requests**: Maximum 10 parallel requests

### Optimization Tips

1. **Caching**: Enable result caching for repeated searches
2. **Batch Processing**: Process multiple matches in batches
3. **Async Processing**: Use async methods for I/O operations
4. **Result Pagination**: Implement pagination for large result sets

### Performance Metrics

- **Search Time**: Average 2-5 seconds per search
- **Matching Time**: Average 1-3 seconds per match calculation
- **Dashboard Generation**: Average 0.5-1 seconds
- **End-to-End Workflow**: Average 10-15 seconds

## Security

### API Key Management

- Store API keys in environment variables
- Use `.env` files for local development
- Never commit API keys to version control
- Rotate API keys regularly

### Data Privacy

- All user data is processed in memory only
- No persistent storage of personal information
- API calls are encrypted in transit
- Optional audit logging available

## Support and Troubleshooting

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

1. **API Key Errors**: Verify environment variables are set
2. **Timeout Errors**: Increase timeout values in configuration
3. **Rate Limits**: Implement exponential backoff
4. **Memory Issues**: Process results in smaller batches

### Getting Help

- GitHub Issues: [https://github.com/skkuhg/intellimatch-pro/issues](https://github.com/skkuhg/intellimatch-pro/issues)
- Documentation: [docs/](../)
- Examples: [EXAMPLES.md](EXAMPLES.md)

---

*For more detailed examples and advanced usage, see the [Examples Documentation](EXAMPLES.md).*