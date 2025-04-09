from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from app.gemini import generate_interview_questions
from app.supabase_client import supabase
import json

router = APIRouter()

class InterviewRequest(BaseModel):
    role: str
    level: str
    techstack: str
    type: str
    amount: int
    email: EmailStr

@router.post("/generate-and-save")
async def generate_and_save(data: InterviewRequest):
    result_text = await generate_interview_questions(
        data.role, data.level, data.techstack, data.type, data.amount
    )

    try:
        questions = json.loads(result_text)
    except:
        questions = [result_text]

    record = {
        "role": data.role,
        "level": data.level,
        "techstack": data.techstack,
        "type": data.type,
        "amount": data.amount,
        "questions": json.dumps(questions),
        "email": data.email
    }

    print("Record to insert:", record)
    response = supabase.table("interview_questions").insert(record).execute()
    print("Insert response:", response)
    return {"message": "Saved successfully", "questions": questions}
