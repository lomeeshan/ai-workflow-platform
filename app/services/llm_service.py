import os
import json
from dotenv import load_dotenv
from groq import Groq

from app.schemas import TaskAnalysis


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_task_with_llm(title: str, description: str) -> TaskAnalysis:
    """
    Sends a task to Groq and asks the model to return structured task analysis.

    This function is intentionally isolated from the route layer.
    If we later switch from Groq to another provider, we only need to change this file.
    """

    system_message = """
    You are an AI assistant inside a productivity/workflow platform.

    Your job is to analyze user tasks and return structured JSON only.

    You must classify the task using the allowed values.

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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    raw_output = response.choices[0].message.content

    try:
        parsed_output = json.loads(raw_output)
    except json.JSONDecodeError:
        raise ValueError(f"Groq returned invalid JSON: {raw_output}")

    return TaskAnalysis(**parsed_output)
