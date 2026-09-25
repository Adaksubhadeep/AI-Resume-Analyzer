import json
import re
from groq import Groq
from src.config import Config
from src.models import AnalysisReport

class GroqLLMClient:
    def __init__(self):
        Config.validate()
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL

    def analyze_resume(self, resume_text: str, job_description: str) -> AnalysisReport:
        prompt = f"""
You are an expert technical recruiter and ATS software evaluator.
Analyze the provided resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY a single valid JSON object adhering strictly to this schema:
{{
    "ats_score": integer (0-100),
    "candidate_summary": "string",
    "matched_skills": ["string"],
    "missing_skills": ["string"],
    "partial_match_skills": ["string"],
    "strengths": ["string"],
    "weaknesses": ["string"],
    "experience_match": "string",
    "education_match": "string",
    "project_match": "string",
    "resume_improvements": ["string"],
    "interview_questions": ["string (10 total)"]
}}
Do not include markdown code block tags or extra explanation outside the JSON.
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a specialized ATS analyzer outputting purely valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        raw_content = response.choices[0].message.content
        cleaned_json = self._clean_json_string(raw_content)
        data = json.loads(cleaned_json)
        return AnalysisReport(**data)

    def generate_general_tips(self, resume_text: str) -> str:
        prompt = f"""
Review this resume as a hiring manager. Provide 8 actionable recommendations to make it stand out.
Focus on quantifiable achievements, clarity, ATS compatibility, and phrasing.

RESUME:
{resume_text}
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert executive resume reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content

    @staticmethod
    def _clean_json_string(content: str) -> str:
        content = content.strip()
        content = re.sub(r"^```json\s*", "", content, flags=re.IGNORECASE)
        content = re.sub(r"^```\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
        return content.strip()