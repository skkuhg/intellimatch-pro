# IntelliMatch Pro - Usage Examples

This document provides comprehensive examples of how to use IntelliMatch Pro for various job matching and talent discovery scenarios.

## Table of Contents

1. [Basic Setup](#basic-setup)
2. [Job Seeker Examples](#job-seeker-examples)
3. [Recruiter Examples](#recruiter-examples)
4. [Advanced Analytics](#advanced-analytics)
5. [Custom Workflows](#custom-workflows)
6. [Integration Examples](#integration-examples)

## Basic Setup

### Environment Configuration

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API keys are set
required_keys = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
for key in required_keys:
    if not os.getenv(key):
        raise ValueError(f"Missing required environment variable: {key}")

print("✅ Environment configured successfully!")
```

### Basic Imports

```python
from src.models.job_seeker import JobSeeker
from src.models.job_posting import JobPosting
from src.engines.search_engine import LinkedInSearchEngine
from src.engines.matching_engine import MatchingEngine
from src.workflows.job_matching_workflow import create_job_matching_workflow
from src.utils.analytics import JobMatchingAnalytics

# Initialize components
search_engine = LinkedInSearchEngine(os.getenv("TAVILY_API_KEY"))
matching_engine = MatchingEngine()
analytics = JobMatchingAnalytics()
workflow = create_job_matching_workflow()
```

## Job Seeker Examples

### Example 1: Entry-Level Software Developer

```python
# Create job seeker profile
entry_level_dev = JobSeeker(
    skills=[
        "Python", "JavaScript", "HTML", "CSS", "Git",
        "React", "SQL", "Problem Solving"
    ],
    experience_years=1,
    education_level="Bachelor's in Computer Science",
    preferred_salary_range="$60,000 - $80,000",
    preferred_location="Remote or San Francisco Bay Area",
    preferred_job_types=["Full-time", "Internship"],
    career_goals="Grow into a full-stack developer role with opportunities to learn new technologies"
)

# Run job matching workflow
results = workflow.invoke({
    "request_type": "job_seeker",
    "user_input": entry_level_dev.dict()
})

# Display results
print(f"Found {len(results['matches'])} job matches")
for match in results['matches'][:3]:  # Show top 3
    print(f"\n🎯 {match['title']} at {match['company']}")
    print(f"   Compatibility: {match['compatibility_score']:.1%}")
    print(f"   Location: {match['location']}")
    print(f"   Salary: {match['salary_range']}")
    print(f"   Why it's a good fit: {match['explanation'][:100]}...")
```

### Example 2: Career Transition - Teacher to UX Designer

```python
# Career changer profile
career_changer = JobSeeker(
    skills=[
        "Communication", "Problem Solving", "Research",
        "Adobe Creative Suite", "Figma", "User Research",
        "Prototyping", "Project Management"
    ],
    experience_years=5,  # Teaching experience
    education_level="Master's in Education + UX Bootcamp",
    preferred_salary_range="$70,000 - $90,000",
    preferred_location="Austin, TX or Remote",
    preferred_job_types=["Full-time"],
    career_goals="Transition from education to UX design, leveraging teaching skills in user empathy and communication"
)

# Run workflow with career transition context
results = workflow.invoke({
    "request_type": "job_seeker",
    "user_input": career_changer.dict(),
    "context": "career_transition"
})

# Generate transition insights
transition_insights = analytics.analyze_career_transition(
    current_profile=career_changer,
    target_field="UX Design",
    job_matches=results['matches']
)

print("🔄 Career Transition Analysis:")
print(f"   Transferable Skills: {', '.join(transition_insights['transferable_skills'])}")
print(f"   Skills to Develop: {', '.join(transition_insights['skills_gap'])}")
print(f"   Recommended Certifications: {', '.join(transition_insights['certifications'])}")
```

### Example 3: Senior Data Scientist

```python
# Senior professional profile
senior_data_scientist = JobSeeker(
    skills=[
        "Python", "R", "Machine Learning", "Deep Learning",
        "TensorFlow", "PyTorch", "SQL", "Apache Spark",
        "AWS", "Docker", "Kubernetes", "Statistics",
        "Data Visualization", "Leadership", "Mentoring"
    ],
    experience_years=8,
    education_level="PhD in Statistics",
    preferred_salary_range="$150,000 - $200,000",
    preferred_location="New York, Seattle, or Remote",
    preferred_job_types=["Full-time"],
    career_goals="Lead data science teams and drive AI strategy at a tech company"
)

# Advanced matching with leadership focus
results = workflow.invoke({
    "request_type": "job_seeker",
    "user_input": senior_data_scientist.dict(),
    "focus_areas": ["leadership", "strategy", "team_management"]
})

# Generate leadership insights
leadership_analysis = analytics.analyze_leadership_potential(
    profile=senior_data_scientist,
    job_matches=results['matches']
)

print("👑 Leadership Opportunity Analysis:")
for opportunity in leadership_analysis['opportunities']:
    print(f"   • {opportunity['company']}: {opportunity['leadership_scope']}")
```

## Recruiter Examples

### Example 1: Startup Looking for Full-Stack Developer

```python
# Create job posting
startup_fullstack_role = JobPosting(
    title="Senior Full-Stack Developer",
    company="TechStart Inc.",
    location="Austin, TX (Hybrid)",
    job_type="Full-time",
    salary_range="$100,000 - $130,000 + equity",
    required_skills=[
        "React", "Node.js", "TypeScript", "PostgreSQL",
        "AWS", "Docker", "Git", "Agile Development"
    ],
    experience_required="3-5 years",
    education_required="Bachelor's degree or equivalent experience",
    description="""Join our fast-growing startup as a Senior Full-Stack Developer! 
    You'll be building scalable web applications, working directly with founders, 
    and having significant impact on product direction. We're looking for someone 
    who thrives in a startup environment and wants to grow with the company."""
)

# Find candidates
results = workflow.invoke({
    "request_type": "recruiter",
    "user_input": startup_fullstack_role.dict()
})

# Display candidate matches
print(f"Found {len(results['candidates'])} potential candidates")
for candidate in results['candidates'][:5]:  # Top 5 candidates
    print(f"\n👤 Candidate Profile:")
    print(f"   Experience: {candidate['experience_years']} years")
    print(f"   Key Skills: {', '.join(candidate['top_skills'])}")
    print(f"   Compatibility: {candidate['compatibility_score']:.1%}")
    print(f"   Why they're a good fit: {candidate['explanation'][:100]}...")
    print(f"   Salary Expectation: {candidate.get('salary_expectation', 'Not specified')}")
```

### Example 2: Enterprise Role - DevOps Engineer

```python
# Enterprise job posting
enterprise_devops_role = JobPosting(
    title="Senior DevOps Engineer",
    company="Enterprise Corp",
    location="San Francisco, CA",
    job_type="Full-time",
    salary_range="$140,000 - $180,000",
    required_skills=[
        "Kubernetes", "Docker", "AWS", "Terraform",
        "Jenkins", "Monitoring", "Security", "Python",
        "Linux", "Networking", "CI/CD"
    ],
    experience_required="5+ years",
    education_required="Bachelor's in Computer Science or related field",
    description="""Lead our DevOps transformation initiative at a Fortune 500 company. 
    You'll be responsible for modernizing our infrastructure, implementing 
    best practices, and mentoring junior engineers."""
)

# Advanced candidate search with cultural fit analysis
results = workflow.invoke({
    "request_type": "recruiter",
    "user_input": enterprise_devops_role.dict(),
    "cultural_fit_criteria": {
        "company_size_preference": "large",
        "industry_experience": "enterprise",
        "leadership_experience": True
    }
})

# Cultural fit analysis
cultural_analysis = analytics.analyze_cultural_fit(
    job_posting=enterprise_devops_role,
    candidates=results['candidates']
)

print("🏢 Cultural Fit Analysis:")
for candidate in cultural_analysis['best_cultural_fits'][:3]:
    print(f"   • Candidate {candidate['id']}: {candidate['cultural_fit_score']:.1%} fit")
    print(f"     Strengths: {', '.join(candidate['cultural_strengths'])}")
```

### Example 3: Remote Team Expansion

```python
# Remote-first company job posting
remote_product_manager = JobPosting(
    title="Senior Product Manager",
    company="RemoteFirst Co.",
    location="Remote (Global)",
    job_type="Full-time",
    salary_range="$120,000 - $150,000",
    required_skills=[
        "Product Strategy", "Agile", "User Research",
        "Data Analysis", "Communication", "Leadership",
        "Remote Work", "Cross-cultural Communication"
    ],
    experience_required="4+ years in product management",
    education_required="Bachelor's degree",
    description="""Join our globally distributed team as a Senior Product Manager. 
    You'll lead product initiatives across multiple time zones and work with 
    diverse, remote teams to deliver exceptional user experiences."""
)

# Global talent search
results = workflow.invoke({
    "request_type": "recruiter",
    "user_input": remote_product_manager.dict(),
    "search_scope": "global",
    "remote_work_criteria": {
        "timezone_flexibility": True,
        "async_communication": True,
        "cultural_adaptability": True
    }
})

# Global diversity analysis
diversity_analysis = analytics.analyze_candidate_diversity(
    candidates=results['candidates'],
    dimensions=["location", "background", "experience"]
)

print("🌍 Global Talent Pool Analysis:")
print(f"   Countries represented: {diversity_analysis['countries_count']}")
print(f"   Time zones covered: {diversity_analysis['timezone_spread']}")
print(f"   Remote work experience: {diversity_analysis['remote_experience_avg']:.1f} years")
```

## Advanced Analytics

### Market Intelligence Dashboard

```python
# Generate comprehensive market insights
market_insights = analytics.generate_market_intelligence(
    job_category="Software Development",
    location="San Francisco",
    time_period="last_6_months"
)

# Create interactive dashboard
dashboard = analytics.create_market_dashboard(market_insights)
dashboard.show()

# Key insights summary
print("📊 Market Intelligence Summary:")
print(f"   Average Salary: {market_insights['avg_salary']}")
print(f"   Most In-Demand Skills: {', '.join(market_insights['top_skills'])}")
print(f"   Hiring Velocity: {market_insights['hiring_velocity']}")
print(f"   Competition Level: {market_insights['competition_level']}")
```

### Skill Gap Analysis

```python
# Analyze skill gaps in the market
skill_analysis = analytics.analyze_skill_gaps(
    job_seekers=results['job_seekers'],
    job_postings=results['job_postings'],
    industry="Technology"
)

# Generate skill development recommendations
recommendations = analytics.generate_skill_recommendations(
    skill_gaps=skill_analysis['gaps'],
    learning_preferences=["online", "hands-on", "certification"]
)

print("🎯 Skill Gap Analysis:")
for gap in skill_analysis['critical_gaps']:
    print(f"   • {gap['skill']}: {gap['demand_supply_ratio']:.2f}x demand")
    print(f"     Learning Path: {gap['recommended_path']}")
```

### Salary Benchmarking

```python
# Comprehensive salary analysis
salary_analysis = analytics.analyze_salary_trends(
    position="Data Scientist",
    location="New York",
    experience_range=(3, 7),
    company_sizes=["startup", "mid-size", "enterprise"]
)

# Generate salary visualization
salary_viz = analytics.create_salary_visualization(salary_analysis)
salary_viz.show()

print("💰 Salary Benchmarking Results:")
print(f"   Market Average: {salary_analysis['market_average']}")
print(f"   Top 25% Earners: {salary_analysis['top_quartile']}")
print(f"   Growth Trajectory: {salary_analysis['growth_rate']:.1%} annually")
```

## Custom Workflows

### Bulk Candidate Processing

```python
# Process multiple candidates efficiently
candidates_batch = [
    {"name": "Alice Johnson", "skills": ["Python", "ML"], "experience": 4},
    {"name": "Bob Smith", "skills": ["React", "Node.js"], "experience": 3},
    {"name": "Carol Davis", "skills": ["DevOps", "AWS"], "experience": 6}
]

job_posting = enterprise_devops_role  # From previous example

# Batch processing workflow
batch_results = []
for candidate_data in candidates_batch:
    candidate = JobSeeker(
        skills=candidate_data["skills"],
        experience_years=candidate_data["experience"],
        # ... other fields with defaults
    )
    
    match_result = matching_engine.calculate_job_compatibility(
        job_seeker=candidate,
        job_posting=job_posting
    )
    
    batch_results.append({
        "candidate": candidate_data["name"],
        "compatibility": match_result.compatibility_score,
        "explanation": match_result.explanation
    })

# Sort by compatibility
batch_results.sort(key=lambda x: x["compatibility"], reverse=True)

print("📋 Batch Processing Results:")
for result in batch_results:
    print(f"   {result['candidate']}: {result['compatibility']:.1%} compatibility")
```

### A/B Testing Different Matching Algorithms

```python
# Compare different matching approaches
def test_matching_algorithms():
    test_cases = [
        {"job_seeker": entry_level_dev, "job_posting": startup_fullstack_role},
        {"job_seeker": senior_data_scientist, "job_posting": enterprise_devops_role}
    ]
    
    algorithms = [
        {"name": "Standard", "temperature": 0.1, "weights": {"skills": 0.4, "experience": 0.3, "culture": 0.3}},
        {"name": "Skill-Focused", "temperature": 0.0, "weights": {"skills": 0.6, "experience": 0.2, "culture": 0.2}},
        {"name": "Balanced", "temperature": 0.2, "weights": {"skills": 0.33, "experience": 0.33, "culture": 0.34}}
    ]
    
    results = {}
    for algo in algorithms:
        results[algo["name"]] = []
        for test_case in test_cases:
            # Configure matching engine with algorithm parameters
            matching_engine.configure(algo)
            match = matching_engine.calculate_job_compatibility(
                test_case["job_seeker"], test_case["job_posting"]
            )
            results[algo["name"]].append(match.compatibility_score)
    
    # Compare results
    for algo_name, scores in results.items():
        avg_score = sum(scores) / len(scores)
        print(f"   {algo_name} Algorithm: {avg_score:.1%} average compatibility")

test_matching_algorithms()
```

## Integration Examples

### Webhook Integration

```python
# Example webhook handler for real-time job notifications
def handle_new_job_webhook(job_data):
    """Process incoming job posting webhook"""
    
    # Parse job posting
    job_posting = JobPosting(**job_data)
    
    # Find matching candidates from database
    matching_candidates = search_engine.find_matching_candidates(
        job_posting=job_posting,
        candidate_pool="active_job_seekers"
    )
    
    # Calculate compatibility scores
    for candidate in matching_candidates:
        match_result = matching_engine.calculate_candidate_compatibility(
            candidate=candidate,
            job_posting=job_posting
        )
        
        # Send notification if high compatibility
        if match_result.compatibility_score > 0.8:
            send_match_notification(
                candidate_id=candidate.id,
                job_posting=job_posting,
                match_score=match_result.compatibility_score
            )
    
    return {"processed_candidates": len(matching_candidates)}

# Example usage
job_webhook_data = {
    "title": "AI Engineer",
    "company": "AI Startup",
    "location": "Remote",
    "required_skills": ["Python", "TensorFlow", "MLOps"]
    # ... other fields
}

result = handle_new_job_webhook(job_webhook_data)
print(f"Processed {result['processed_candidates']} candidates")
```

### CRM Integration

```python
# Example Salesforce CRM integration
class CRMIntegration:
    def __init__(self, crm_client):
        self.crm = crm_client
        self.matching_engine = MatchingEngine()
    
    def sync_candidates_with_jobs(self):
        """Sync CRM opportunities with candidate matches"""
        
        # Get open job opportunities from CRM
        open_jobs = self.crm.get_open_opportunities()
        
        for job_opp in open_jobs:
            # Convert CRM data to JobPosting
            job_posting = self.crm_to_job_posting(job_opp)
            
            # Find candidates
            candidates = search_engine.search_candidates(job_posting)
            
            # Calculate matches
            matches = []
            for candidate in candidates:
                match = self.matching_engine.calculate_candidate_compatibility(
                    candidate, job_posting
                )
                if match.compatibility_score > 0.7:
                    matches.append(match)
            
            # Update CRM with match data
            self.crm.update_opportunity_with_matches(
                opportunity_id=job_opp['id'],
                matches=matches
            )
        
        return {"jobs_processed": len(open_jobs)}
    
    def crm_to_job_posting(self, crm_opportunity):
        """Convert CRM opportunity to JobPosting model"""
        return JobPosting(
            title=crm_opportunity['title'],
            company=crm_opportunity['account_name'],
            location=crm_opportunity['location'],
            required_skills=crm_opportunity['required_skills'].split(','),
            # ... map other fields
        )

# Example usage
# crm_client = SalesforceClient()
# crm_integration = CRMIntegration(crm_client)
# result = crm_integration.sync_candidates_with_jobs()
# print(f"Synced {result['jobs_processed']} job opportunities")
```

### Email Campaign Integration

```python
# Example email campaign for matched candidates
def create_personalized_job_alert_campaign():
    """Create personalized email campaign for job matches"""
    
    # Get active job seekers
    active_seekers = get_active_job_seekers()
    
    # Get new job postings
    new_jobs = get_recent_job_postings(days=7)
    
    email_campaigns = []
    
    for seeker in active_seekers:
        # Find relevant jobs
        relevant_jobs = []
        for job in new_jobs:
            match = matching_engine.calculate_job_compatibility(seeker, job)
            if match.compatibility_score > 0.75:
                relevant_jobs.append({
                    "job": job,
                    "match_score": match.compatibility_score,
                    "explanation": match.explanation
                })
        
        # Create personalized email if jobs found
        if relevant_jobs:
            email_content = generate_personalized_email(
                seeker=seeker,
                job_matches=relevant_jobs
            )
            
            email_campaigns.append({
                "recipient": seeker.email,
                "subject": f"🎯 {len(relevant_jobs)} Perfect Job Matches Found!",
                "content": email_content
            })
    
    return email_campaigns

def generate_personalized_email(seeker, job_matches):
    """Generate personalized email content"""
    email_template = f"""
    Hi {seeker.name},
    
    Great news! We found {len(job_matches)} jobs that are perfect matches for your profile:
    
    """
    
    for match in job_matches[:3]:  # Top 3 matches
        job = match['job']
        email_template += f"""
        🎯 {job.title} at {job.company}
        📍 {job.location}
        💰 {job.salary_range}
        🎯 {match['match_score']:.0%} compatibility
        💡 Why it's perfect: {match['explanation'][:100]}...
        
        """
    
    email_template += """
    Ready to apply? Click the links above or visit our platform for more details.
    
    Best regards,
    The IntelliMatch Pro Team
    """
    
    return email_template

# Generate campaign
campaign = create_personalized_job_alert_campaign()
print(f"Created {len(campaign)} personalized email alerts")
```

---

## Tips for Best Results

### For Job Seekers
1. **Be Specific**: Provide detailed skills and clear career goals
2. **Update Regularly**: Keep your profile current with new skills and experience
3. **Use Keywords**: Include industry-relevant terms and technologies
4. **Be Realistic**: Set achievable salary and location preferences

### For Recruiters
1. **Detailed Job Descriptions**: Include specific requirements and company culture
2. **Clear Expectations**: Specify experience levels and must-have skills
3. **Competitive Positioning**: Highlight unique benefits and opportunities
4. **Regular Updates**: Keep job postings current and relevant

### For Optimal Performance
1. **API Rate Limits**: Monitor API usage to avoid rate limiting
2. **Batch Processing**: Use batch operations for large datasets
3. **Caching**: Enable caching for frequently accessed data
4. **Error Handling**: Implement robust error handling and retries

---

*For more examples and advanced use cases, check the [API Documentation](API.md) and [System Architecture](ARCHITECTURE.md) guides.*