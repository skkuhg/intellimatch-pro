# IntelliMatch Pro - Source Code Structure

## Data Models

### JobSeeker Model
```python
from pydantic import BaseModel, Field
from typing import List, Optional

class JobSeeker(BaseModel):
    """Job seeker profile model"""
    skills: List[str] = Field(..., description="List of skills and competencies")
    experience_years: int = Field(..., ge=0, description="Years of professional experience")
    education_level: str = Field(..., description="Highest education level")
    preferred_salary_range: Optional[str] = Field(None, description="Expected salary range")
    preferred_location: Optional[str] = Field(None, description="Preferred work location")
    preferred_job_types: List[str] = Field(default=["Full-time"], description="Preferred employment types")
    career_goals: Optional[str] = Field(None, description="Career objectives and goals")
    
    class Config:
        json_schema_extra = {
            "example": {
                "skills": ["Python", "Machine Learning", "Data Analysis"],
                "experience_years": 3,
                "education_level": "Bachelor's in Computer Science",
                "preferred_salary_range": "$80,000 - $120,000",
                "preferred_location": "Remote",
                "preferred_job_types": ["Full-time"],
                "career_goals": "Transition to AI/ML engineering role"
            }
        }
```

### JobPosting Model
```python
class JobPosting(BaseModel):
    """Job posting model"""
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    job_type: str = Field(..., description="Employment type")
    salary_range: Optional[str] = Field(None, description="Salary range")
    required_skills: List[str] = Field(..., description="Required skills and technologies")
    experience_required: str = Field(..., description="Required experience level")
    education_required: str = Field(..., description="Required education level")
    description: str = Field(..., description="Detailed job description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Senior Data Scientist",
                "company": "TechCorp Inc.",
                "location": "San Francisco, CA",
                "job_type": "Full-time",
                "salary_range": "$130,000 - $180,000",
                "required_skills": ["Python", "TensorFlow", "Statistics"],
                "experience_required": "5+ years",
                "education_required": "Master's in related field",
                "description": "Leading data science projects and mentoring junior staff"
            }
        }
```

## Search Engine Implementation

```python
import asyncio
from typing import List, Dict, Any
from langchain_community.tools.tavily_search import TavilySearchResults

class LinkedInSearchEngine:
    """Advanced LinkedIn search engine using Tavily AI"""
    
    def __init__(self, tavily_api_key: str):
        self.search_tool = TavilySearchResults(
            api_key=tavily_api_key,
            max_results=50,
            search_depth="advanced",
            include_domains=["linkedin.com"],
            include_answer=True
        )
    
    async def search_jobs(self, job_seeker: JobSeeker) -> List[Dict[str, Any]]:
        """Search for job opportunities matching job seeker profile"""
        query = self._build_job_search_query(job_seeker)
        
        try:
            results = await self._execute_search(query)
            return self._process_job_results(results, job_seeker)
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def _build_job_search_query(self, job_seeker: JobSeeker) -> str:
        """Build optimized search query for jobs"""
        skills_str = " OR ".join(job_seeker.skills[:5])  # Top 5 skills
        location_str = job_seeker.preferred_location or "remote"
        
        query = f"""
        site:linkedin.com/jobs 
        ("{skills_str}") 
        "{location_str}" 
        "{job_seeker.experience_years} years experience"
        """
        
        return query.strip()
    
    async def _execute_search(self, query: str) -> List[Dict]:
        """Execute search with retry logic"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                return self.search_tool.run(query)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Matching Engine Implementation

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict, List
import json

class MatchingEngine:
    """AI-powered job matching engine"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=2000
        )
        self.job_seeker_prompt = self._create_job_seeker_prompt()
        self.recruiter_prompt = self._create_recruiter_prompt()
    
    def _create_job_seeker_prompt(self) -> ChatPromptTemplate:
        """Create prompt template for job seeker matching"""
        return ChatPromptTemplate.from_messages([
            ("system", """
            You are an expert career counselor and job matching specialist. 
            Analyze the compatibility between a job seeker and job opportunities.
            
            Provide detailed analysis including:
            1. Overall compatibility score (0-100%)
            2. Skill alignment assessment
            3. Experience level fit
            4. Career growth potential
            5. Specific recommendations
            
            Return your analysis in the following JSON format:
            {
                "compatibility_score": float,
                "skill_match_percentage": float,
                "experience_fit": string,
                "salary_alignment": string,
                "growth_potential": string,
                "explanation": string,
                "recommendations": [string]
            }
            """),
            ("human", """
            Job Seeker Profile:
            Skills: {skills}
            Experience: {experience_years} years
            Education: {education_level}
            Salary Expectation: {preferred_salary_range}
            Location Preference: {preferred_location}
            Career Goals: {career_goals}
            
            Job Opportunity:
            Title: {job_title}
            Company: {company}
            Location: {job_location}
            Required Skills: {required_skills}
            Experience Required: {experience_required}
            Salary Range: {salary_range}
            Description: {job_description}
            
            Please analyze this match and provide your assessment.
            """)
        ])
    
    async def calculate_job_compatibility(
        self, 
        job_seeker: JobSeeker, 
        job_posting: JobPosting
    ) -> Dict[str, Any]:
        """Calculate compatibility between job seeker and job posting"""
        
        prompt_values = {
            "skills": ", ".join(job_seeker.skills),
            "experience_years": job_seeker.experience_years,
            "education_level": job_seeker.education_level,
            "preferred_salary_range": job_seeker.preferred_salary_range or "Not specified",
            "preferred_location": job_seeker.preferred_location or "Flexible",
            "career_goals": job_seeker.career_goals or "Not specified",
            "job_title": job_posting.title,
            "company": job_posting.company,
            "job_location": job_posting.location,
            "required_skills": ", ".join(job_posting.required_skills),
            "experience_required": job_posting.experience_required,
            "salary_range": job_posting.salary_range or "Not specified",
            "job_description": job_posting.description
        }
        
        try:
            response = await self.llm.ainvoke(
                self.job_seeker_prompt.format_messages(**prompt_values)
            )
            
            # Parse JSON response
            result = json.loads(response.content)
            
            # Add metadata
            result.update({
                "job_seeker_id": id(job_seeker),
                "job_posting_id": id(job_posting),
                "analysis_timestamp": datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            print(f"Matching error: {e}")
            return self._create_fallback_match(job_seeker, job_posting)
    
    def _create_fallback_match(self, job_seeker: JobSeeker, job_posting: JobPosting) -> Dict:
        """Create basic compatibility score when AI analysis fails"""
        # Simple skill overlap calculation
        job_skills = set(skill.lower() for skill in job_posting.required_skills)
        seeker_skills = set(skill.lower() for skill in job_seeker.skills)
        
        skill_overlap = len(job_skills.intersection(seeker_skills))
        skill_match_percentage = (skill_overlap / len(job_skills)) * 100 if job_skills else 0
        
        return {
            "compatibility_score": min(skill_match_percentage / 100, 1.0),
            "skill_match_percentage": skill_match_percentage,
            "experience_fit": "Basic analysis - AI unavailable",
            "salary_alignment": "Unable to analyze",
            "growth_potential": "Unable to analyze",
            "explanation": f"Basic skill match: {skill_overlap}/{len(job_skills)} required skills found",
            "recommendations": ["Complete profile analysis requires AI service"]
        }
```

## Analytics Implementation

```python
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict, Any

class JobMatchingAnalytics:
    """Advanced analytics for job matching insights"""
    
    def generate_job_seeker_dashboard(self, matches: List[Dict]) -> go.Figure:
        """Create comprehensive job seeker dashboard"""
        
        # Create subplot layout
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Compatibility Scores Distribution',
                'Top Skills in Demand',
                'Salary Range Analysis',
                'Location Distribution'
            ),
            specs=[
                [{"type": "histogram"}, {"type": "bar"}],
                [{"type": "box"}, {"type": "pie"}]
            ]
        )
        
        # Extract data from matches
        compatibility_scores = [match.get('compatibility_score', 0) * 100 for match in matches]
        skills_demand = self._analyze_skill_demand(matches)
        salary_ranges = self._extract_salary_data(matches)
        locations = self._extract_location_data(matches)
        
        # 1. Compatibility scores histogram
        fig.add_trace(
            go.Histogram(
                x=compatibility_scores,
                nbinsx=10,
                name="Compatibility",
                marker_color="lightblue"
            ),
            row=1, col=1
        )
        
        # 2. Top skills bar chart
        fig.add_trace(
            go.Bar(
                x=list(skills_demand.keys())[:10],
                y=list(skills_demand.values())[:10],
                name="Skill Demand",
                marker_color="lightgreen"
            ),
            row=1, col=2
        )
        
        # 3. Salary range box plot
        if salary_ranges:
            fig.add_trace(
                go.Box(
                    y=salary_ranges,
                    name="Salary Range",
                    marker_color="orange"
                ),
                row=2, col=1
            )
        
        # 4. Location pie chart
        if locations:
            location_counts = pd.Series(locations).value_counts()
            fig.add_trace(
                go.Pie(
                    labels=location_counts.index[:5],
                    values=location_counts.values[:5],
                    name="Locations"
                ),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title_text="🎯 Job Seeker Analytics Dashboard",
            title_x=0.5,
            height=600,
            showlegend=False
        )
        
        return fig
    
    def _analyze_skill_demand(self, matches: List[Dict]) -> Dict[str, int]:
        """Analyze skill demand from job matches"""
        skill_counts = {}
        
        for match in matches:
            required_skills = match.get('required_skills', [])
            for skill in required_skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Sort by demand
        return dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True))
    
    def create_compatibility_matrix(self, results: List[Dict]) -> go.Figure:
        """Create compatibility matrix visualization"""
        
        # Prepare data for heatmap
        job_titles = [r.get('job_title', f'Job {i}') for i, r in enumerate(results)]
        compatibility_scores = [r.get('compatibility_score', 0) * 100 for r in results]
        skill_matches = [r.get('skill_match_percentage', 0) for r in results]
        
        # Create matrix data
        matrix_data = [
            compatibility_scores,
            skill_matches,
            [abs(cs - sm) for cs, sm in zip(compatibility_scores, skill_matches)]  # Gap analysis
        ]
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix_data,
            x=job_titles,
            y=['Overall Compatibility', 'Skill Match', 'Gap Analysis'],
            colorscale='RdYlGn',
            text=[[f'{val:.1f}%' for val in row] for row in matrix_data],
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='🎯 Job Compatibility Matrix',
            xaxis_title='Job Opportunities',
            yaxis_title='Match Criteria',
            height=400
        )
        
        return fig
```

## Workflow Implementation

```python
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
from typing import Dict, Any, Optional, List

class WorkflowState(TypedDict):
    """State schema for job matching workflow"""
    request_type: str
    user_input: Dict[str, Any]
    search_results: List[Dict]
    enhanced_data: List[Dict]
    processed_data: Dict[str, Any]
    final_output: Dict[str, Any]
    error_message: Optional[str]

def create_job_matching_workflow() -> StateGraph:
    """Create the main job matching workflow using LangGraph"""
    
    workflow = StateGraph(WorkflowState)
    
    # Add workflow nodes
    workflow.add_node("process_user_input", process_user_input)
    workflow.add_node("search_linkedin_profiles", search_linkedin_profiles)
    workflow.add_node("enhance_search_data", enhance_search_data)
    workflow.add_node("calculate_matches", calculate_matches)
    workflow.add_node("generate_recommendations", generate_recommendations)
    workflow.add_node("format_final_output", format_final_output)
    
    # Define workflow edges
    workflow.set_entry_point("process_user_input")
    workflow.add_edge("process_user_input", "search_linkedin_profiles")
    workflow.add_edge("search_linkedin_profiles", "enhance_search_data")
    workflow.add_edge("enhance_search_data", "calculate_matches")
    workflow.add_edge("calculate_matches", "generate_recommendations")
    workflow.add_edge("generate_recommendations", "format_final_output")
    workflow.add_edge("format_final_output", END)
    
    return workflow.compile()

async def process_user_input(state: WorkflowState) -> WorkflowState:
    """Process and validate user input"""
    try:
        request_type = state["request_type"]
        user_input = state["user_input"]
        
        # Validate input based on request type
        if request_type == "job_seeker":
            validated_input = JobSeeker(**user_input)
        elif request_type == "recruiter":
            validated_input = JobPosting(**user_input)
        else:
            raise ValueError(f"Invalid request type: {request_type}")
        
        return {
            **state,
            "user_input": validated_input.dict(),
            "error_message": None
        }
        
    except Exception as e:
        return {
            **state,
            "error_message": f"Input validation error: {str(e)}"
        }

async def search_linkedin_profiles(state: WorkflowState) -> WorkflowState:
    """Search for relevant profiles/jobs on LinkedIn"""
    try:
        search_engine = LinkedInSearchEngine(os.getenv("TAVILY_API_KEY"))
        request_type = state["request_type"]
        user_input = state["user_input"]
        
        if request_type == "job_seeker":
            job_seeker = JobSeeker(**user_input)
            results = await search_engine.search_jobs(job_seeker)
        else:  # recruiter
            job_posting = JobPosting(**user_input)
            results = await search_engine.search_candidates(job_posting)
        
        return {
            **state,
            "search_results": results,
            "error_message": None
        }
        
    except Exception as e:
        return {
            **state,
            "search_results": [],
            "error_message": f"Search error: {str(e)}"
        }
```

---

*This source code structure provides a solid foundation for the IntelliMatch Pro system. Each component is designed to be modular, testable, and scalable.*