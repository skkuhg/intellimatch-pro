import pytest
from pydantic import ValidationError
from src.models.job_seeker import JobSeeker
from src.models.job_posting import JobPosting
from src.models.match_result import MatchResult

class TestJobSeekerModel:
    """Test JobSeeker data model"""
    
    def test_valid_job_seeker_creation(self):
        """Test creating a valid job seeker"""
        job_seeker = JobSeeker(
            skills=["Python", "Machine Learning"],
            experience_years=3,
            education_level="Bachelor's",
            preferred_salary_range="$80,000 - $120,000",
            preferred_location="Remote",
            preferred_job_types=["Full-time"],
            career_goals="Become a senior data scientist"
        )
        
        assert job_seeker.skills == ["Python", "Machine Learning"]
        assert job_seeker.experience_years == 3
        assert job_seeker.education_level == "Bachelor's"
    
    def test_job_seeker_required_fields(self):
        """Test that required fields are enforced"""
        with pytest.raises(ValidationError):
            JobSeeker()  # Missing required fields
        
        with pytest.raises(ValidationError):
            JobSeeker(skills=[])  # Empty skills list
    
    def test_job_seeker_experience_validation(self):
        """Test experience years validation"""
        with pytest.raises(ValidationError):
            JobSeeker(
                skills=["Python"],
                experience_years=-1,  # Negative experience
                education_level="Bachelor's"
            )
    
    def test_job_seeker_optional_fields(self):
        """Test optional fields with defaults"""
        job_seeker = JobSeeker(
            skills=["Python"],
            experience_years=2,
            education_level="Bachelor's"
        )
        
        assert job_seeker.preferred_job_types == ["Full-time"]
        assert job_seeker.preferred_salary_range is None
        assert job_seeker.career_goals is None

class TestJobPostingModel:
    """Test JobPosting data model"""
    
    def test_valid_job_posting_creation(self):
        """Test creating a valid job posting"""
        job_posting = JobPosting(
            title="Data Scientist",
            company="TechCorp",
            location="San Francisco",
            job_type="Full-time",
            salary_range="$100,000 - $140,000",
            required_skills=["Python", "Statistics"],
            experience_required="2-4 years",
            education_required="Bachelor's",
            description="Join our data science team"
        )
        
        assert job_posting.title == "Data Scientist"
        assert job_posting.company == "TechCorp"
        assert "Python" in job_posting.required_skills
    
    def test_job_posting_required_fields(self):
        """Test that all required fields are enforced"""
        with pytest.raises(ValidationError):
            JobPosting(title="Data Scientist")  # Missing other required fields
    
    def test_job_posting_empty_skills(self):
        """Test that empty required skills list is invalid"""
        with pytest.raises(ValidationError):
            JobPosting(
                title="Data Scientist",
                company="TechCorp",
                location="San Francisco",
                job_type="Full-time",
                required_skills=[],  # Empty skills
                experience_required="2+ years",
                education_required="Bachelor's",
                description="Job description"
            )

class TestMatchResultModel:
    """Test MatchResult data model"""
    
    def test_valid_match_result_creation(self):
        """Test creating a valid match result"""
        match_result = MatchResult(
            job_seeker_id="seeker_123",
            job_posting_id="job_456",
            compatibility_score=0.85,
            explanation="Strong technical skills alignment",
            skill_match_percentage=80.0,
            experience_fit="Good fit",
            salary_alignment="Within range",
            recommendations=["Apply immediately", "Highlight ML experience"]
        )
        
        assert match_result.compatibility_score == 0.85
        assert match_result.skill_match_percentage == 80.0
        assert len(match_result.recommendations) == 2
    
    def test_compatibility_score_validation(self):
        """Test compatibility score range validation"""
        # Valid scores
        MatchResult(
            job_seeker_id="seeker_123",
            job_posting_id="job_456",
            compatibility_score=0.0,  # Min valid
            explanation="No match",
            skill_match_percentage=0.0,
            experience_fit="Poor fit",
            salary_alignment="Below range",
            recommendations=[]
        )
        
        MatchResult(
            job_seeker_id="seeker_123",
            job_posting_id="job_456",
            compatibility_score=1.0,  # Max valid
            explanation="Perfect match",
            skill_match_percentage=100.0,
            experience_fit="Perfect fit",
            salary_alignment="Exact match",
            recommendations=["Immediate hire"]
        )
        
        # Invalid scores
        with pytest.raises(ValidationError):
            MatchResult(
                job_seeker_id="seeker_123",
                job_posting_id="job_456",
                compatibility_score=1.5,  # Too high
                explanation="Invalid",
                skill_match_percentage=50.0,
                experience_fit="Good",
                salary_alignment="Good",
                recommendations=[]
            )
        
        with pytest.raises(ValidationError):
            MatchResult(
                job_seeker_id="seeker_123",
                job_posting_id="job_456",
                compatibility_score=-0.1,  # Too low
                explanation="Invalid",
                skill_match_percentage=50.0,
                experience_fit="Good",
                salary_alignment="Good",
                recommendations=[]
            )
    
    def test_skill_match_percentage_validation(self):
        """Test skill match percentage validation"""
        with pytest.raises(ValidationError):
            MatchResult(
                job_seeker_id="seeker_123",
                job_posting_id="job_456",
                compatibility_score=0.5,
                explanation="Test",
                skill_match_percentage=150.0,  # Too high
                experience_fit="Good",
                salary_alignment="Good",
                recommendations=[]
            )
        
        with pytest.raises(ValidationError):
            MatchResult(
                job_seeker_id="seeker_123",
                job_posting_id="job_456",
                compatibility_score=0.5,
                explanation="Test",
                skill_match_percentage=-10.0,  # Too low
                experience_fit="Good",
                salary_alignment="Good",
                recommendations=[]
            )