from pydantic import BaseModel, Field
from typing import List

class AnalysisReport(BaseModel):
    ats_score: int = Field(..., ge=0, le=100, description="Overall ATS compatibility score from 0 to 100")
    candidate_summary: str = Field(..., description="Brief overview of candidate profile relative to the job")
    matched_skills: List[str] = Field(default_factory=list, description="Skills present in both resume and JD")
    missing_skills: List[str] = Field(default_factory=list, description="Key required skills missing from the resume")
    partial_match_skills: List[str] = Field(default_factory=list, description="Related or tangentially demonstrated skills")
    strengths: List[str] = Field(default_factory=list, description="Core candidate strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Key candidate gaps or areas of concern")
    experience_match: str = Field(..., description="Evaluation of past experience relevance")
    education_match: str = Field(..., description="Evaluation of education alignment")
    project_match: str = Field(..., description="Evaluation of candidate project work")
    resume_improvements: List[str] = Field(default_factory=list, description="Actionable bullet points to improve resume")
    interview_questions: List[str] = Field(default_factory=list, description="10 tailored technical/behavioral interview questions")