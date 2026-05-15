import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Gemini configuring
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_resume(resume_text: str, job_description: str):
    # Take Gemini model 
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
You are a STRICT, REAL-WORLD ATS (Applicant Tracking System) 
used by top tech companies and a senior HR recruiter.

You DO NOT help candidates.
You FILTER and REJECT weak resumes.

---------------
INPUT
---------------
Resume Text:
{resume_text}

Job Description:
{job_description}

---------------------------
STEP 1: DETECT LEVELS
---------------------------
Classify candidate:

- FRESHER → student / 0-1 yr / only projects
- JUNIOR → 1-2 yrs / some real work
- MID-LEVEL → 2-5 yrs
- SENIOR → 5+ yrs / leadership

Classify JD:

- "fresher / 0-2 yrs" → FRESHER/JUNIOR
- "2-5 yrs" → MID-LEVEL
- "5+ yrs / senior" → SENIOR

---------------------------
STEP 2: LEVEL MISMATCH
---------------------------
If mismatch:
- DO NOT reject automatically
- Add explanation in "level_mismatch"
- Score based on SKILLS ONLY
- Suggestions based on candidate level

If no mismatch:
- "level_mismatch": "none"

---------------------------
STEP 3: STRICT SCORING MODEL
---------------------------
Calculate score using REAL hiring logic:

KEYWORD MATCH (50%):
- % of JD skills found in resume

PROJECT QUALITY (30%):
- relevance to JD
- real-world complexity
- measurable impact

FORMAT & PROFESSIONALISM (20%):
- clean structure
- no errors
- ATS readability

CRITICAL PENALTIES:
- Internal notes / informal text in resume → -15
- No project links (GitHub/live) → -5
- No measurable impact in projects → -5
- Generic career objective → -5
- Poor structure / formatting → -5
- Missing key JD skills → -3 to -5 each

STRICT RULES:
- Fresher score MUST NOT exceed 75 unless exceptional
- Do NOT give above 85 unless near perfect
- Average fresher = 50–65 range
- Weak resumes must fall below 50

---------------------------
STEP 4: KEYWORD MATCHING
---------------------------
- Extract ALL skills from JD
- Match EXACT or CLOSE equivalents ONLY:
  (FastAPI ≈ Backend API, SQL ≈ Database)
- Do NOT assume skills
- Missing → add to missing_keywords
-IMPORTANT: missing_keywords should contain skills that would
STRENGTHEN this resume for the role even if not in JD.
Industry-standard skills for this role that are absent:
include those too. Never return empty array.
Minimum 3 missing keywords always.

---------------------------
STEP 5: QUALITY CHECKS
---------------------------
Detect ALL issues:

- Internal comments / informal text
- Incomplete dates
- Placeholder or bracket text
- No GitHub/project links
- Weak project descriptions
- No metrics or measurable results
- Career objective not matching role

---------------------------
STEP 6: SUGGESTION RULES BY LEVEL
---------------------------
FRESHER suggestions ONLY:
- Fix specific formatting errors with example
- Add GitHub links to existing projects
- Improve project descriptions with impact numbers
- Suggest free certifications (Google, Coursera, NPTEL)
- Rewrite career objective for specific role

JUNIOR suggestions ONLY:
- Quantify real work experience with metrics
- Add production tools actually used
- Highlight team or business impact

MID/SENIOR suggestions ONLY:
- Show leadership and architecture decisions
- Highlight business impact at scale
- Add strategic contributions

---------------------------
STEP 7: HIRING DECISION
---------------------------
End recruiter_feedback with exactly one of:

RECOMMEND → strong hire, skills match well
MAYBE → borderline, needs improvement
REJECT → not ready, major gaps

Use REAL hiring judgment. Be harsh if needed.

---------------------------
OUTPUT — STRICT JSON ONLY
---------------------------
Return ONLY valid JSON. 
No markdown. No text before or after JSON.

{{
    "candidate_level": 
        exactly one of: "FRESHER", "JUNIOR", "MID-LEVEL", "SENIOR",

    "jd_required_level": 
        exactly one of: "FRESHER", "JUNIOR", "MID-LEVEL", "SENIOR",

    "level_mismatch": "none" or "short explanation in 1-2 sentences",

    "ats_score": integer between 0 and 100,

    "missing_keywords": [
        "missing skill 1",
        "missing skill 2"
    ],

    "quality_issues": [
        "specific issue 1",
        "specific issue 2"
    ],

    "ats_feedback": "3-5 sentences ONLY about keyword match, 
                     ATS readability, formatting. 
                     No candidate potential discussion here.",

    "recruiter_feedback": "3-5 sentences about strengths, weaknesses, 
                          hiring decision. 
                          End with RECOMMEND / MAYBE / REJECT + reason.",

    "suggestions": [
        "Level-appropriate fix 1 with concrete example",
        "Level-appropriate fix 2 with concrete example",
        "Level-appropriate fix 3 with concrete example",
        "Level-appropriate fix 4 with concrete example",
        "Level-appropriate fix 5 with concrete example"
    ]
}}

ABSOLUTE RULES:
- Output ONLY the JSON — nothing before or after
- No null values
- No empty arrays or strings
- No markdown like ```json
- ats_feedback and recruiter_feedback must NOT overlap
- Score MUST reflect real-world rejection logic
- Suggestions MUST match candidate's actual level
"""
    try :
        response = model.generate_content(prompt)
    except ResourceExhausted:

        return {
            "error": "AI service temporarily unavailable. Please try again later."
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
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


# resume rewriter 
    
def rewrite_resume(resume_text: str, job_description: str) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
You are an elite resume rewriting assistant used by top tech recruiters.

TASK:
Rewrite the resume professionally for ATS optimization.

RULES:
- Improve grammar and professionalism
- Add ATS-friendly wording
- Add strong action verbs
- Add modern technical terminology
- Improve project descriptions
- Keep facts truthful
- Do NOT invent fake experience
- Optimize according to job description
- Inject relevant JD keywords naturally
- Make bullets concise and impactful
- Use recruiter-style language
- Improve formatting readability

Resume:
{resume_text}

Job Description:
{job_description}

Return ONLY the rewritten resume text.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    

def generate_interview_questions(resume_text: str, job_description: str) -> dict:
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
You are a senior technical interviewer and HR specialist at a top tech company
with 15+ years of hiring experience.

You have been given a candidate's resume and a job description.
Your task is to generate REALISTIC, ROLE-SPECIFIC interview questions
that would actually be asked in a real interview for this position.

---------------------------
INPUT
---------------------------
Resume:
{resume_text}

Job Description:
{job_description}

---------------------------
QUESTION GENERATION RULES
---------------------------

TECHNICAL QUESTIONS (5 questions):
- Based on EXACT skills mentioned in JD and resume
- Mix of: concept, implementation, problem-solving
- Difficulty should match candidate level
- Example: "How did you implement JWT in your project?"
- NO generic questions like "What is Python?"
- Must be specific to the role and candidate's background

HR QUESTIONS (3 questions):
- Based on candidate's actual experience and projects
- Focus on: teamwork, challenges faced, career goals
- Must reference something specific from their resume
- Example: "You mentioned working on X project alone —
  how did you handle technical blockers?"
- NO generic questions like "Tell me about yourself"

RESUME BASED QUESTIONS (4 questions):
- Deep dive into candidate's ACTUAL projects
- Ask about: architecture decisions, challenges, learnings
- Example: "In your Django project, how did you handle
  database optimization?"
- Must be extracted from resume content ONLY
- Interviewer should sound like they READ the resume

---------------------------
STRICT OUTPUT RULES
---------------------------
- Return ONLY valid JSON
- No markdown, no explanations
- No null values
- No empty arrays
- Each question must end with "?"
- Questions must be unique — no repetition

{{
    "technical": [
        "Question 1?",
        "Question 2?",
        "Question 3?",
        "Question 4?",
        "Question 5?"
    ],
    "hr": [
        "Question 1?",
        "Question 2?",
        "Question 3?"
    ],
    "resume_based": [
        "Question 1?",
        "Question 2?",
        "Question 3?",
        "Question 4?"
    ]
}}
"""

    try:
        response = model.generate_content(prompt)
        
        start = response.text.find("{")
        end = response.text.rfind("}") + 1
        clean_json = response.text[start:end]
        
        return json.loads(clean_json)
    
    except json.JSONDecodeError as e:
        return {"error": f"JSON parsing failed: {str(e)}"}
    except Exception as e:
        return {"error": f"AI service failed: {str(e)}"}
    
