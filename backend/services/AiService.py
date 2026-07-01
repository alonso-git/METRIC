from openai import AsyncOpenAI
from config import settings

async_client = AsyncOpenAI(api_key=settings.api_key)


async def run_data_tool(msg: str) -> str:
    # Use a clear, restrictive system prompt
    system_prompt = (
        "You are a NLP tool. "
        "Your only task is to extract the user intent and feeling from the provided "
        "message string and provide a brief recommendation for an agent to support that "
        "client, as short as for someone in a live phone call to read and apply it. "
        "Output ONLY raw JSON in the format:"
        ""
        "Do not include conversational text, markdown, or explanations."
    )

    response = await async_client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": msg}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    
    if not response.choices[0].message.content:
        return "Unknown"
    else:
        return response.choices[0].message.content