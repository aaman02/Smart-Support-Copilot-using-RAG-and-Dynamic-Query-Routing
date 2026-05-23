from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

from modules.prompts import (
    TROUBLESHOOT_PROMPT,
    COMPARISON_PROMPT,
    GENERAL_PROMPT
)

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv(
        "AZURE_OPENAI_CHAT_DEPLOYMENT"
    ),
    api_version=os.getenv(
        "AZURE_OPENAI_API_VERSION"
    ),
    azure_endpoint=os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    ),
    api_key=os.getenv(
        "AZURE_OPENAI_API_KEY"
    ),
    temperature=0
)


def generate_response(
    query,
    query_type,
    docs,
    chat_history
):

    history = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in chat_history
        ]
    )

    if query_type == "troubleshooting":
        prompt = TROUBLESHOOT_PROMPT

    elif query_type == "comparison":
        prompt = COMPARISON_PROMPT

    else:
        prompt = GENERAL_PROMPT

    final_prompt = prompt.format(
        chat_history=history,
        context=docs,
        query=query
    )

    response = llm.invoke(final_prompt)

    return response.content