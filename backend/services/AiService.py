from typing import Any

from google import genai
from entities import AnalysisResult, message_response
from config import settings
from entities import analysis_result_ai_response
from sqlalchemy.orm import Session

# 1. Initialize the new SDK client (sync and async are handled through the same client object)
client = genai.Client(api_key=settings.api_key)

async def run_message_analysis(msg: message_response, db: Session) -> analysis_result_ai_response | None:
    schema = analysis_result_ai_response.model_json_schema()

    system_prompt = (
        "You are a NLP tool. "
        "Your only task is to extract the user intent and feeling from the provided "
        "message string and provide a brief recommendation for an agent to support that "
        "client, as short as for someone in a live phone call to read and apply it. " \
        "The response content must match the language in which you received the raw message. "
        "Output ONLY raw JSON in the format:"
        "Do not include conversational text, markdown, or explanations."
    )

    try:
        # 2. Use the async client (.aio) and properly group the parameters
        interaction: Any = await client.aio.interactions.create(
            model="gemini-3.5-flash",
            input=msg.raw,
            system_instruction=system_prompt,
            # Schema and MIME type MUST be grouped in response_format
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": schema
            },
            # Temperature and token limits MUST be grouped in generation_config
            generation_config={
                "temperature": 0.3
            }
        )

        answer = interaction.output_text
        answer = answer if answer else ''
        
        analysis = analysis_result_ai_response.model_validate_json(answer)
        
        db_analysis = AnalysisResult(
            message_id = msg.id,
            intent = analysis.intent,
            recommendations = analysis.recommendations
        )
        db.add(db_analysis)
        
        return analysis

    except Exception as e:
        print(f"AI is dumb, dude: {e}")
        return None