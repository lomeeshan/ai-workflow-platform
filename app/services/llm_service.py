import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from app.schemas import TaskAnalysis
from app.exceptions import LLMServiceError, InvalidLLMResponseError


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise LLMServiceError("GROQ_API_KEY is not configured.")

client = Groq(api_key=GROQ_API_KEY)


def analyze_task_with_llm(title: str, description: str) -> TaskAnalysis:
    system_message = """
    You are an AI assistant inside a productivity/workflow platform.

    Your job is to analyze user tasks and return structured JSON only.

    Allowed categories:
    - school
    - career
    - personal
    - finance
    - health
    - technical
    - other

    Allowed priorities:
    - low
    - medium
    - high

    Allowed estimated_effort values:
    - small
    - medium
    - large

    Return only valid JSON.
    Do not include markdown.
    Do not include explanations outside the JSON.
    """

    user_message = f"""
    Analyze this task:

    Title: {title}

    Description: {description}

    Return JSON with exactly these fields:
    - category
    - priority
    - estimated_effort
    - summary
    - reasoning
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

    except Exception as e:
        raise LLMServiceError("Failed to get response from Groq.") from e

    raw_output = response.choices[0].message.content

    try:
        parsed_output = json.loads(raw_output)

    except json.JSONDecodeError as e:
        raise InvalidLLMResponseError("Groq returned invalid JSON.") from e

    try:
        return TaskAnalysis(**parsed_output)

    except ValidationError as e:
        raise InvalidLLMResponseError("Groq returned JSON that does not match the expected schema.") from e
