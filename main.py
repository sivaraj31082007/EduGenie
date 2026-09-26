import os
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from google import genai


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini client
client = None

if API_KEY and API_KEY != "YOUR_GEMINI_API_KEY":
    client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="EduGenie",
    description="AI Educational Assistant",
    version="1.0.0"
)


# --------------------------------------------------
# TEMPLATES & STATIC FILES
# --------------------------------------------------

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# --------------------------------------------------
# GEMINI FUNCTION
# --------------------------------------------------

def ask_gemini(prompt: str) -> str:

    if client is None:
        return (
            "Gemini API key is not configured. "
            "Please add your GEMINI_API_KEY in the .env file."
        )

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"AI Error: {str(e)}"


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "EduGenie"
        }
    )


# --------------------------------------------------
# ASK AI
# --------------------------------------------------

@app.post("/ask")
async def ask_ai(question: str = Form(...)):

    prompt = f"""
You are EduGenie, a friendly AI educational assistant.

Answer the student's question clearly and simply.

Question:
{question}

Give:
1. Simple explanation
2. Important points
3. Example if needed
"""

    answer = ask_gemini(prompt)

    return {
        "success": True,
        "answer": answer
    }


# --------------------------------------------------
# EXPLAIN TOPIC
# --------------------------------------------------

@app.post("/explain")
async def explain_topic(topic: str = Form(...)):

    prompt = f"""
Explain the following topic to a college student.

Topic:
{topic}

Use very simple language.

Structure:
- Definition
- Simple explanation
- Key points
- Real-world example
- Short summary
"""

    answer = ask_gemini(prompt)

    return {
        "success": True,
        "answer": answer
    }


# --------------------------------------------------
# GENERATE QUIZ
# --------------------------------------------------

@app.post("/quiz")
async def generate_quiz(
    topic: str = Form(...),
    number: int = Form(5)
):

    prompt = f"""
Create a quiz for the topic:

{topic}

Generate {number} multiple-choice questions.

For every question provide:

Question:
A)
B)
C)
D)

Correct Answer:
Explanation:

Keep the questions suitable for college students.
"""

    answer = ask_gemini(prompt)

    return {
        "success": True,
        "answer": answer
    }


# --------------------------------------------------
# LEARNING PATH
# --------------------------------------------------

@app.post("/learning-path")
async def learning_path(topic: str = Form(...)):

    prompt = f"""
Create a step-by-step learning path for:

{topic}

Create a beginner-friendly roadmap.

Include:

1. Beginner concepts
2. Basic concepts
3. Intermediate concepts
4. Advanced concepts
5. Practice activities
6. Mini project ideas
7. Final revision

Keep it simple and practical.
"""

    answer = ask_gemini(prompt)

    return {
        "success": True,
        "answer": answer
    }


# --------------------------------------------------
# SUMMARIZE TEXT
# --------------------------------------------------

@app.post("/summarize")
async def summarize_text(text: str = Form(...)):

    prompt = f"""
Summarize the following educational text.

Text:
{text}

Give:

- Short summary
- Important points
- Key terms
- 5 quick revision points

Use simple language.
"""

    answer = ask_gemini(prompt)

    return {
        "success": True,
        "answer": answer
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
async def health_check():

    return {
        "status": "EduGenie is running",
        "gemini_configured": client is not None
    }


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )