import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Gemini configuring
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_resume(resume_text: str, job_description: str):
    # Take Gemini model 
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
                You are an expert ATS (Applicant Tracking System) and professional HR recruiter.

                You will be given:
                1. Resume Text
                2. Job Description

                Your task is to strictly analyze the resume against the job description.

                Resume Text:
                {resume_text}

                Job Description:
                {job_description}

                Return ONLY valid JSON. Do NOT include markdown, explanations, headings, or extra text.

                STRICT OUTPUT FORMAT:
                {{
                    "ats_score": integer (0-100),

                    "missing_keywords": [
                        "string", "string"
                    ],

                    "ats_feedback": "2-4 concise sentences focusing on keyword match, formatting, and relevance",

                    "recruiter_feedback": "2-4 concise sentences including both strengths and weaknesses from a recruiter’s perspective",

                    "suggestions": [
                        "Actionable improvement 1",
                        "Actionable improvement 2",
                        "Actionable improvement 3",
                        "Actionable improvement 4"
                    ]
                }}

                RULES:
                - ats_score must be an integer between 0 and 100
                - missing_keywords must be a list of important missing skills/tools
                - suggestions must be actionable and specific
                - Do not return null values
                - Do not add any text outside JSON
                """
    response = model.generate_content(prompt)
    
    start = response.text.find("{")
    end = response.text.rfind("}") + 1
    
    clean_json = response.text[start:end]

    try:
        data = json.loads(clean_json)
        return data
    
    except json.JSONDecodeError as e:
        return {"error": f"JSON parsing failed: {str(e)}"}
    except Exception as e:
            return {"error": f"AI service failed: {str(e)}"}