from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from app.gemini import generate_interview_questions
from app.supabase_client import supabase
from app.routes.interview import router as interview_router
import json
import os  # ✅ Added import

app = FastAPI()
app.include_router(interview_router)


class InterviewRequest(BaseModel):
    role: str
    level: str
    techstack: str
    type: str
    amount: int
    email: EmailStr


@app.post("/generate-questions")
async def generate(data: InterviewRequest):
    questions_raw = await generate_interview_questions(
        data.role, data.level, data.techstack, data.type, data.amount
    )
    try:
        questions = json.loads(questions_raw)
    except json.JSONDecodeError:
        questions = [q.strip() for q in questions_raw.split("\n") if q.strip()]

    supabase.table("interview_questions").insert({
        "role": data.role,
        "level": data.level,
        "techstack": data.techstack,
        "type": data.type,
        "amount": data.amount,
        "questions": questions,
        "email": data.email
    }).execute()

    return {"questions": questions}


# ✅ Add this block to run with uvicorn when deployed directly
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
