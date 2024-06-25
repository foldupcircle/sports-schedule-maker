import os
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

from langchain_openai import ChatOpenAI

GPT3 = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo",
    temperature=0
)

GPT4 = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4-1106-preview",
    temperature=0
)
