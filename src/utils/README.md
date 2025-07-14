# IntelliMatch Pro - Utility Functions

This directory contains shared utility functions and helper modules used throughout the system.

## Utilities

- `data_processing.py`: Data cleaning and transformation utilities
- `api_helpers.py`: API client helpers and retry logic
- `validation.py`: Input validation and sanitization
- `caching.py`: Result caching and optimization
- `logging.py`: Structured logging configuration
- `metrics.py`: Performance metrics collection

## Features

### Data Processing
- Text normalization and cleaning
- Skill extraction and standardization
- Salary parsing and normalization
- Location geocoding and standardization

### API Helpers
- Exponential backoff retry logic
- Rate limiting compliance
- Connection pooling
- Error handling and logging

### Caching
- In-memory result caching
- TTL-based cache expiration
- Cache key generation
- Memory-efficient storage

### Validation
- Input sanitization
- Type checking and conversion
- Business rule validation
- Error message generation

## Usage

```python
from src.utils.data_processing import normalize_skills
from src.utils.api_helpers import retry_with_backoff
from src.utils.caching import cached_result
from src.utils.validation import validate_job_seeker

# Normalize skills
clean_skills = normalize_skills(["python", "machine-learning", "AI"])

# Retry API calls
result = await retry_with_backoff(api_call, max_retries=3)

# Cache expensive operations
@cached_result(ttl=3600)
def expensive_calculation(data):
    return process_data(data)
```