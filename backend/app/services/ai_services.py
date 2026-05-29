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
used by top tech companies and senior HR recruiters.

You are NOT a career coach.
You are NOT supportive.
You FILTER weak resumes aggressively.

Your job is to simulate REAL hiring logic.

---

## INPUT

Resume Text:
{resume_text}

Job Description:
{job_description}

---

## STEP 1: DETECT CANDIDATE LEVEL

Classify candidate level ONLY from evidence in resume:

* FRESHER → student / internship / projects only / 0-1 year
* JUNIOR → 1-2 years practical work
* MID-LEVEL → 2-5 years industry experience
* SENIOR → 5+ years leadership/architecture ownership

Classify JD required level:

* "intern", "fresher", "0-2 years" → FRESHER/JUNIOR
* "2-5 years" → MID-LEVEL
* "5+ years", "senior", "lead" → SENIOR

---

## STEP 2: LEVEL MISMATCH CHECK

If experience level mismatches:

* DO NOT automatically reject
* Mention mismatch clearly in "level_mismatch"
* Still score based on skills and project quality
* Suggestions must remain appropriate to candidate level

If no mismatch:
"level_mismatch": "none"

---

## STEP 3: STRICT ATS SCORING MODEL

Calculate ATS score using REAL hiring logic.

TOTAL SCORE = 100

1. KEYWORD MATCH = 50%
2. PROJECT QUALITY = 30%
3. FORMAT & ATS READABILITY = 20%

---

## STEP 3.1: KEYWORD MATCH RULES

Extract ALL technical and professional skills from JD.

ONLY match:

* exact skills
* close equivalents

Examples:

* FastAPI ≈ backend API framework
* SQL ≈ database querying
* JWT ≈ authentication system

DO NOT assume skills.
DO NOT hallucinate technologies.

If resume does not explicitly mention a skill,
consider it MISSING.

---

## STEP 3.2: SKILL PRIORITY WEIGHTING

Classify skills into:

CRITICAL SKILLS:
Core technologies directly required for role.

IMPORTANT SKILLS:
Deployment, databases, APIs, testing, DevOps.

BONUS SKILLS:
Optional frameworks/tools/nice-to-have items.

SCORING IMPACT:

* Missing CRITICAL skill → -8 to -12
* Missing IMPORTANT skill → -4 to -6
* Missing BONUS skill → -1 to -3

Examples:

Backend Role:
CRITICAL:
Python, Django, FastAPI, APIs

IMPORTANT:
PostgreSQL, MongoDB, Docker, Authentication

BONUS:
Tailwind, AWS, CI/CD, Redis

---

## STEP 3.3: PROJECT QUALITY RULES

Evaluate projects based on:

* technical complexity
* relevance to JD
* real-world practicality
* deployment experience
* authentication/security
* databases
* scalability
* APIs
* AI/ML integration if applicable

Higher score ONLY if:

* projects are technically meaningful
* project descriptions are detailed
* measurable outcomes exist
* GitHub/live links exist

---

## STEP 3.4: FORMAT & ATS READABILITY

Check:

* clean formatting
* ATS readability
* grammar
* professionalism
* section organization
* consistency

Penalize:

* informal text
* internal notes
* poor formatting
* missing sections
* unclear structure

---

## STEP 4: STRICT PENALTIES

Apply realistic recruiter penalties:

* Internal comments/informal text → -15
* No GitHub/project links → -5
* No measurable project impact → -5
* Generic career objective → -5
* Weak formatting → -5
* Missing CRITICAL skills → severe penalty
* Missing IMPORTANT skills → moderate penalty

---

## STEP 5: STRICT SCORE LIMITS

IMPORTANT REALISM RULES:

* Average fresher resumes = 50-65
* Strong fresher resumes = 65-75
* Exceptional fresher resumes = max 80
* NEVER give above 85 unless near perfect
* Weak resumes MUST fall below 50

DO NOT inflate scores.

---

## STEP 6: QUALITY ISSUE DETECTION

Detect ALL issues including:

* missing GitHub links
* missing deployment links
* no metrics in projects
* weak project descriptions
* incomplete dates
* placeholder text
* generic objective
* inconsistent formatting
* ATS-unfriendly structure

---

## STEP 7: RESUME STRENGTHS

Extract REAL strengths ONLY from evidence.

DO NOT use fake praise.

Avoid generic phrases like:

* "excellent candidate"
* "impressive profile"
* "strong engineer"

Every strength MUST be supported by:

* projects
* technologies
* deployment
* architecture
* measurable impact

---

## STEP 8: SUGGESTIONS BY LEVEL

FRESHER suggestions:

* add GitHub links
* improve project descriptions
* add metrics
* improve career objective
* suggest certifications
* suggest deployment improvements

JUNIOR suggestions:

* quantify work impact
* highlight production systems
* add business impact

MID/SENIOR suggestions:

* leadership impact
* architecture decisions
* scaling systems
* strategic contributions

Suggestions MUST:

* be specific
* contain concrete examples
* contain actionable fixes
* avoid vague advice

---

## STEP 9: HIRING DECISION

Use REAL recruiter judgment.

RECOMMEND:

* strong alignment
* good projects
* few critical gaps

MAYBE:

* decent profile but noticeable gaps
* requires screening

REJECT:

* weak profile
* major missing skills
* poor projects
* poor ATS readiness

IMPORTANT:
End recruiter_feedback with EXACTLY ONE:

* RECOMMEND
* MAYBE
* REJECT

---

## OUTPUT FORMAT

Return ONLY VALID JSON.

No markdown.
No explanation.
No extra text.

{{
"candidate_level": "FRESHER/JUNIOR/MID-LEVEL/SENIOR",


"jd_required_level": "FRESHER/JUNIOR/MID-LEVEL/SENIOR",

"level_mismatch": "none or short explanation",

"ats_score": integer,

"section_scores": {{
    "keyword_match": integer,
    "project_quality": integer,
    "formatting": integer,
    "ats_readability": integer
}},

"strengths": [
    "strength 1",
    "strength 2",
    "strength 3"
],

"missing_keywords": [
    "missing skill 1",
    "missing skill 2",
    "missing skill 3"
],

"quality_issues": [
    "issue 1",
    "issue 2"
],

"ats_feedback": "3-5 sentences ONLY about ATS, keyword match, formatting, readability.",

"recruiter_feedback": "3-5 sentences ONLY about hiring evaluation and recruiter judgment. End with RECOMMEND or MAYBE or REJECT.",

"suggestions": [
    "specific actionable suggestion 1",
    "specific actionable suggestion 2",
    "specific actionable suggestion 3",
    "specific actionable suggestion 4",
    "specific actionable suggestion 5"
]
```

}}

---

## ABSOLUTE RULES

* Output ONLY JSON
* No markdown
* No null values
* No empty arrays
* No hallucinated skills
* No duplicate feedback
* ats_feedback and recruiter_feedback MUST differ
* Suggestions MUST match candidate level
* Use harsh but realistic hiring logic
  
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

IMPORTANT FORMATTING RULES:
- Do NOT use markdown (no **, no *, no #)
- Use CAPS for section headings only
- Use plain text bullets with dash (-)
- Plain text only — no special characters

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
---------------
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
    
