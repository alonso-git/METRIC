import json
import httpx
from entities import AnalysisResult, analysis_result_ai_response
from config import settings
from sqlalchemy.orm import Session

API_URL = "https://opencode.ai/zen/go/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are an NLP tool embedded in a customer support chat system. "
    "Your only task is to analyze the user message and output a JSON object "
    "with two fields:\n"
    '  "intent"      — a short label describing what the customer wants or feels\n'
    '  "recommendations" — a brief suggestion for the support agent on how to reply\n'
    "Respond in the same language as the customer's message. "
    "Output ONLY the JSON object, no markdown, no explanations."
)


async def run_message_analysis(msg, db: Session) -> analysis_result_ai_response | None:
    payload = {
        "model": "deepseek-v4-pro",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": msg.raw},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.3,
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.api_key}",
                },
                json=payload,
            )

        if response.status_code != 200:
            print(f"AI API error ({response.status_code}): {response.text[:200]}")
            return None

        content = response.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        analysis = analysis_result_ai_response.model_validate(parsed)

        db_analysis = AnalysisResult(
            message_id=msg.id,
            intent=analysis.intent,
            recommendations=analysis.recommendations,
        )
        db.add(db_analysis)

        return analysis

    except Exception as e:
        print(f"AI analysis skipped: {e}")
        return None
