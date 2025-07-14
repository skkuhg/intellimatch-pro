# IntelliMatch Pro - LangGraph Workflows

This directory contains LangGraph workflow implementations for complex job matching processes.

## Workflows

- `job_matching_workflow.py`: Main job matching workflow
- `candidate_sourcing_workflow.py`: Recruiter candidate sourcing workflow
- `analytics_workflow.py`: Analytics generation workflow
- `notification_workflow.py`: Real-time notification workflow

## Workflow Architecture

### Job Matching Workflow
```
Input Processing → LinkedIn Search → Data Enhancement → 
Compatibility Scoring → Recommendations → Output Formatting
```

### State Management
- Typed state schemas using TypedDict
- Error handling and recovery
- Parallel processing capabilities
- Workflow monitoring and tracing

## Features

- **Async Processing**: Non-blocking workflow execution
- **Error Recovery**: Automatic retry and fallback mechanisms
- **State Persistence**: Workflow state management
- **Monitoring**: LangSmith integration for observability

## Usage

```python
from src.workflows.job_matching_workflow import create_job_matching_workflow

# Create and run workflow
workflow = create_job_matching_workflow()
results = await workflow.ainvoke({
    "request_type": "job_seeker",
    "user_input": job_seeker_data
})
```