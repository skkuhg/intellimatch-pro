import pytest
import os
from unittest.mock import Mock, AsyncMock
from src.models.job_seeker import JobSeeker
from src.models.job_posting import JobPosting
from src.engines.search_engine import LinkedInSearchEngine
from src.engines.matching_engine import MatchingEngine

# Test configuration
pytest_plugins = ["pytest_asyncio"]

@pytest.fixture(scope="session")
def test_config():
    """Test configuration fixture"""
    return {
        "openai_api_key": os.getenv("TEST_OPENAI_API_KEY", "test_key"),
        "tavily_api_key": os.getenv("TEST_TAVILY_API_KEY", "test_key"),
        "test_mode": True,
        "mock_external_apis": True
    }

@pytest.fixture
def sample_job_seeker():
    """Sample job seeker for testing"""
    return JobSeeker(
        skills=["Python", "Machine Learning", "Data Analysis"],
        experience_years=3,
        education_level="Bachelor's in Computer Science",
        preferred_salary_range="$80,000 - $120,000",
        preferred_location="Remote",
        preferred_job_types=["Full-time"],
        career_goals="Grow into a senior data scientist role"
    )

@pytest.fixture
def sample_job_posting():
    """Sample job posting for testing"""
    return JobPosting(
        title="Data Scientist",
        company="TechCorp Inc.",
        location="San Francisco, CA",
        job_type="Full-time",
        salary_range="$100,000 - $140,000",
        required_skills=["Python", "Statistics", "Machine Learning"],
        experience_required="2-4 years",
        education_required="Bachelor's degree",
        description="Join our data science team to build ML models"
    )

@pytest.fixture
def mock_search_engine(test_config):
    """Mock search engine for testing"""
    engine = LinkedInSearchEngine(test_config["tavily_api_key"])
    engine.search_tool = Mock()
    engine.search_tool.run = AsyncMock(return_value=[
        {
            "title": "Senior Data Scientist",
            "company": "AI Corp",
            "url": "https://linkedin.com/jobs/123",
            "content": "Looking for experienced data scientist..."
        }
    ])
    return engine

@pytest.fixture
def mock_matching_engine():
    """Mock matching engine for testing"""
    engine = MatchingEngine()
    engine.llm = Mock()
    engine.llm.ainvoke = AsyncMock(return_value=Mock(
        content='{"compatibility_score": 0.85, "explanation": "Great match!"}'
    ))
    return engine

@pytest.fixture
def sample_search_results():
    """Sample search results for testing"""
    return [
        {
            "title": "Data Scientist",
            "company": "TechCorp",
            "location": "San Francisco",
            "url": "https://linkedin.com/jobs/1",
            "content": "We're looking for a data scientist..."
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AI Startup",
            "location": "Remote",
            "url": "https://linkedin.com/jobs/2",
            "content": "Join our ML team..."
        }
    ]

@pytest.fixture
def sample_match_results():
    """Sample match results for testing"""
    return [
        {
            "job_seeker_id": "seeker_1",
            "job_posting_id": "job_1",
            "compatibility_score": 0.85,
            "skill_match_percentage": 80.0,
            "experience_fit": "Good fit",
            "salary_alignment": "Within range",
            "explanation": "Strong technical skills match",
            "recommendations": ["Consider applying immediately"]
        },
        {
            "job_seeker_id": "seeker_1",
            "job_posting_id": "job_2",
            "compatibility_score": 0.72,
            "skill_match_percentage": 65.0,
            "experience_fit": "Slight stretch",
            "salary_alignment": "Competitive",
            "explanation": "Good cultural fit, some skill development needed",
            "recommendations": ["Consider with additional training"]
        }
    ]

# Test utilities
class TestHelpers:
    @staticmethod
    def assert_valid_compatibility_score(score):
        """Assert that compatibility score is valid"""
        assert isinstance(score, (int, float))
        assert 0 <= score <= 1
    
    @staticmethod
    def assert_valid_match_result(result):
        """Assert that match result has required fields"""
        required_fields = [
            "compatibility_score",
            "skill_match_percentage",
            "experience_fit",
            "explanation"
        ]
        for field in required_fields:
            assert field in result
        
        TestHelpers.assert_valid_compatibility_score(result["compatibility_score"])
        assert isinstance(result["skill_match_percentage"], (int, float))
        assert 0 <= result["skill_match_percentage"] <= 100

@pytest.fixture
def test_helpers():
    """Test helper utilities"""
    return TestHelpers()