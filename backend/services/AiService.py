from openai import AsyncOpenAI
from config import settings

async_client = AsyncOpenAI(api_key=settings.api_key)


async def run_data_tool(input_data: str) -> str:
    # Use a clear, restrictive system prompt
    system_prompt = (
        "You are a data processing tool. "
        "Your only task is to extract the user ID and status from the provided JSON string. "
        "Output ONLY raw JSON. Do not include conversational text, markdown, or explanations."
    )

    response = await async_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_data}
        ],
        response_format={"type": "json_object"},
        temperature=0,  # CRITICAL: Set to 0 for deterministic output
    )
    
    if not response.choices[0].message.content:
        return "Unknown"
    else:
        return response.choices[0].message.content