from groq import Groq

from src.config import GROQ_API_KEY, GROQ_MODEL


client = Groq(api_key=GROQ_API_KEY)


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
    """
    Calls the Groq-hosted LLM and returns plain text.
    This keeps the rest of the app independent from the provider implementation.
    """

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content