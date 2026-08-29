import ollama


def ask_llm(question, business_context):
    """Ask the local LLM a business question using InsightAI data."""

    prompt = f"""
You are InsightAI, an AI business analyst.

Answer the user's question using ONLY the business
data provided below.

BUSINESS DATA:
{business_context}

USER QUESTION:
{question}

Instructions:
- Give a clear and concise business answer.
- Use the actual numbers from the provided data.
- Do not invent facts.
- If the data is insufficient to answer something,
  clearly say so.
"""

    try:

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as error:

        return (
            "⚠️ **AI service is currently unavailable.**\n\n"
            "Please make sure Ollama is running and the "
            "`llama3.2:3b` model is available.\n\n"
            f"Technical details: `{error}`"
        )