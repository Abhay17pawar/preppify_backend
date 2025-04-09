import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

async def generate_interview_questions(role, level, techstack, type, amount):
    prompt = f"""
    Prepare questions for a job interview.
    The job role is {role}.
    The job experience level is {level}.
    The tech stack used in the job is: {techstack}.
    The focus between behavioural and technical questions should lean towards: {type}.
    The amount of questions required is: {amount}.
    Please return only the questions, without any additional text.
    The questions are going to be read by a voice assistant so do not use '/' or '*' or any special formatting.
    Return the questions formatted like this:
    ["Question 1", "Question 2", "Question 3"]
    """
    response = model.generate_content(prompt)
    return response.text
